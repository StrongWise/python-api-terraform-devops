# VPC(Virtual Private Cloud)
#  - 퍼블릭 클라우드 서비스내에 논리적으로 분리된, 고객 전용 사설 가상 네트워크 공간
# CIDR(Classless Inter-Domain Routing)
#  - CIDR은 네트워크 주소 지정 방식, IPv4 는 8비트씩 4개 그룹, 0~255까지 표기
#  - 네트워크 주소/서브넷 마스크 비트 (ex. 192.168.10.0/24)
#  - 서브넷 마스크 비트가 24면 앞에서부터 24비트가 네트워크, 나머지 8비트가 호스트영역
#  - 실제 사용할수 있는 IP는 192.168.10.1 ~ 192.168.10.254 까지

#### VPC
resource "aws_vpc" "default" {
  cidr_block           = "10.10.0.0/16" # Please set this according to your company size
  enable_dns_hostnames = true

  tags = {
    Name = "vpc-msd-apnortheast2"
  }
}

# 서브넷 종류
#  - 퍼블릭 서브넷 : 외부 접근 가능(ELB같은 외부접속 필요 서버)
#  - NAT를 통하는 프라이빗 서브넷 : 외부 접근 불가, 외부 서버 호출(본인 인증 같은)
#  - 프라이빗 서브넷 : 외부 통신 안함, 필요시 NAT적용 서버 통해 호출(DB나 캐시 접근하는 서버)
#  - 데이터베이스 서브넷 : DB나 캐시 서버만 위치하는 서브넷 대역

#### 퍼블릭 서브넷 자동 생성
resource "aws_subnet" "public" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.default.id

  cidr_block              = "10.${var.cidr_numeral}.${lookup(var.cidr_numeral_public, count.index)}.0/20"
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public${count.index}-${var.vpc_name}"
  }
}

#### 퍼블릭 서브넷용 라우팅 테이블 생성
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.default.id

  tags = {
    Name = "publicrt-${var.vpc_name}"
  }
}

# IGW(Internet Gateway)
# VPC에서 외부와 inbound, outbound 트래픽 처리
resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id

  tags = {
    Name = "igw-${var.vpc_name}"
  }
}

# NAT Gateway
# 프라이빗 서브넷의 outbound 트래픽을 IGW로 연결해 외부로 전달
resource "aws_nat_gateway" "nat" {
  count         = length(var.availability_zones)
  allocation_id = element(aws_eip.nat.*.id, count.index)
  subnet_id     = element(aws_subnet.public.*.id, count.index)

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "NAT-GW${count.index}-${var.vpc_name}"
  }
}

resource "aws_eip" "nat" {
  count  = length(var.availability_zones)
  domain = "vpc"

  lifecycle {
    create_before_destroy = true
  }
}

# 퍼블릭 서브넷용 인터넷 라우트
resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.default.id
}

# 프라이빗 서브넷용 NAT 라우트
resource "aws_route" "private_nat" {
  count                  = length(var.availability_zones)
  route_table_id         = element(aws_route_table.private.*.id, count.index)
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = element(aws_nat_gateway.nat.*.id, count.index)
}

resource "aws_route_table" "private" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.default.id

  tags = {
    Name    = "private${count.index}rt-${var.vpc_name}"
    Network = "Private"
  }
}
