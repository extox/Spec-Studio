/** Pre-built architecture sample YAML templates for the canvas. */

export interface ArchitectureSample {
  id: string;
  name: string;
  description: string;
  icon: string;
  yaml: string;
}

export const ARCHITECTURE_SAMPLES: ArchitectureSample[] = [
  {
    id: "web-3tier",
    name: "3-Tier 웹 시스템",
    description: "클라이언트 → 로드밸런서 → 웹서버 → WAS → DB 구조",
    icon: "🌐",
    yaml: `system_name: "3-Tier 웹 시스템"
system_type: monolith
description: "전통적인 3-Tier 웹 애플리케이션 아키텍처"

boundaries:
  - id: boundary-external
    type: external
    name: External Zone
    color: "#64748b"
    children:
      - client-browser
      - client-mobile
    _position: {x: 20, y: 140}
    _size: {width: 260, height: 280}
  - id: boundary-dmz
    type: dmz
    name: DMZ
    color: "#f59e0b"
    children:
      - lb-main
      - waf-main
    _position: {x: 320, y: 140}
    _size: {width: 260, height: 280}
  - id: boundary-internal
    type: internal
    name: Internal Network
    color: "#10b981"
    children:
      - web-server-1
      - web-server-2
      - was-server-1
      - was-server-2
    _position: {x: 620, y: 100}
    _size: {width: 480, height: 360}
  - id: boundary-data
    type: subnet
    name: Data Zone
    color: "#6366f1"
    children:
      - db-primary
      - db-replica
      - cache-redis
    _position: {x: 1140, y: 140}
    _size: {width: 280, height: 280}

infrastructure:
  - id: client-browser
    type: client
    name: Web Browser
    _position: {x: 40, y: 40}
    _boundary: boundary-external
    connections:
      - target: lb-main
        label: HTTPS
        direction: forward
  - id: client-mobile
    type: client
    name: Mobile App
    _position: {x: 40, y: 140}
    _boundary: boundary-external
    connections:
      - target: lb-main
        label: HTTPS
        direction: forward
  - id: waf-main
    type: firewall
    name: WAF
    technology: AWS WAF
    _position: {x: 40, y: 40}
    _boundary: boundary-dmz
    connections:
      - target: lb-main
        label: Forward
        direction: forward
  - id: lb-main
    type: load-balancer
    name: Load Balancer
    technology: Nginx
    _position: {x: 40, y: 140}
    _boundary: boundary-dmz
    connections:
      - target: web-server-1
        label: HTTP
        direction: forward
      - target: web-server-2
        label: HTTP
        direction: forward
  - id: web-server-1
    type: server
    name: Web Server 1
    technology: Nginx
    _position: {x: 40, y: 40}
    _boundary: boundary-internal
    connections:
      - target: was-server-1
        label: Proxy
        direction: forward
  - id: web-server-2
    type: server
    name: Web Server 2
    technology: Nginx
    _position: {x: 240, y: 40}
    _boundary: boundary-internal
    connections:
      - target: was-server-2
        label: Proxy
        direction: forward
  - id: was-server-1
    type: service
    name: WAS 1
    technology: Spring Boot
    _position: {x: 40, y: 200}
    _boundary: boundary-internal
    connections:
      - target: db-primary
        label: JDBC
        direction: forward
      - target: cache-redis
        label: Redis
        direction: bidirectional
  - id: was-server-2
    type: service
    name: WAS 2
    technology: Spring Boot
    _position: {x: 240, y: 200}
    _boundary: boundary-internal
    connections:
      - target: db-primary
        label: JDBC
        direction: forward
      - target: cache-redis
        label: Redis
        direction: bidirectional
  - id: db-primary
    type: database
    name: DB Primary
    technology: PostgreSQL 15
    _position: {x: 40, y: 40}
    _boundary: boundary-data
    connections:
      - target: db-replica
        label: Replication
        direction: forward
  - id: db-replica
    type: database
    name: DB Replica
    technology: PostgreSQL 15
    _position: {x: 40, y: 160}
    _boundary: boundary-data
  - id: cache-redis
    type: cache
    name: Redis Cache
    technology: Redis 7
    _position: {x: 160, y: 100}
    _boundary: boundary-data

_system_info_position: {x: 20, y: 20}
`,
  },
  {
    id: "microservice",
    name: "마이크로서비스 아키텍처",
    description: "API Gateway → 서비스별 독립 배포, 메시지큐 기반 비동기 통신",
    icon: "🔧",
    yaml: `system_name: "마이크로서비스 플랫폼"
system_type: microservice
description: "서비스별 독립 배포 가능한 마이크로서비스 아키텍처"

boundaries:
  - id: boundary-ingress
    type: dmz
    name: Ingress Layer
    color: "#f59e0b"
    children:
      - api-gateway
      - auth-service
    _position: {x: 20, y: 140}
    _size: {width: 280, height: 260}
  - id: boundary-services
    type: cluster
    name: Service Cluster (K8s)
    color: "#06b6d4"
    children:
      - svc-user
      - svc-order
      - svc-product
      - svc-payment
      - svc-notification
    _position: {x: 340, y: 100}
    _size: {width: 540, height: 380}
  - id: boundary-data
    type: subnet
    name: Data Layer
    color: "#6366f1"
    children:
      - db-user
      - db-order
      - db-product
      - mq-kafka
      - cache-redis
    _position: {x: 920, y: 100}
    _size: {width: 320, height: 380}

infrastructure:
  - id: api-gateway
    type: gateway
    name: API Gateway
    technology: Kong / Nginx
    _position: {x: 40, y: 40}
    _boundary: boundary-ingress
    connections:
      - target: svc-user
        label: REST
      - target: svc-order
        label: REST
      - target: svc-product
        label: REST
  - id: auth-service
    type: service
    name: Auth Service
    technology: Keycloak
    _position: {x: 40, y: 160}
    _boundary: boundary-ingress
  - id: svc-user
    type: service
    name: User Service
    technology: Spring Boot
    _position: {x: 40, y: 40}
    _boundary: boundary-services
    connections:
      - target: db-user
        label: JPA
      - target: mq-kafka
        label: Event Publish
  - id: svc-order
    type: service
    name: Order Service
    technology: Spring Boot
    _position: {x: 220, y: 40}
    _boundary: boundary-services
    connections:
      - target: db-order
        label: JPA
      - target: mq-kafka
        label: Event Publish
      - target: svc-payment
        label: gRPC
  - id: svc-product
    type: service
    name: Product Service
    technology: Node.js
    _position: {x: 400, y: 40}
    _boundary: boundary-services
    connections:
      - target: db-product
        label: Prisma
      - target: cache-redis
        label: Cache
        direction: bidirectional
  - id: svc-payment
    type: service
    name: Payment Service
    technology: Go
    _position: {x: 120, y: 220}
    _boundary: boundary-services
    connections:
      - target: mq-kafka
        label: Event Publish
  - id: svc-notification
    type: service
    name: Notification Service
    technology: Python
    _position: {x: 340, y: 220}
    _boundary: boundary-services
    connections:
      - target: mq-kafka
        label: Event Subscribe
        direction: backward
  - id: db-user
    type: database
    name: User DB
    technology: PostgreSQL
    _position: {x: 40, y: 40}
    _boundary: boundary-data
  - id: db-order
    type: database
    name: Order DB
    technology: PostgreSQL
    _position: {x: 160, y: 40}
    _boundary: boundary-data
  - id: db-product
    type: database
    name: Product DB
    technology: MongoDB
    _position: {x: 40, y: 140}
    _boundary: boundary-data
  - id: mq-kafka
    type: queue
    name: Kafka
    technology: Apache Kafka
    _position: {x: 160, y: 140}
    _boundary: boundary-data
  - id: cache-redis
    type: cache
    name: Redis
    technology: Redis 7
    _position: {x: 100, y: 260}
    _boundary: boundary-data

_system_info_position: {x: 20, y: 20}
`,
  },
  {
    id: "serverless",
    name: "서버리스 아키텍처",
    description: "CloudFront → API Gateway → Lambda → DynamoDB / S3",
    icon: "☁️",
    yaml: `system_name: "서버리스 웹 애플리케이션"
system_type: serverless
description: "AWS 서버리스 기반 웹 애플리케이션"

boundaries:
  - id: boundary-cdn
    type: external
    name: CDN / Edge
    color: "#64748b"
    children:
      - cdn-cloudfront
      - s3-static
    _position: {x: 20, y: 140}
    _size: {width: 260, height: 240}
  - id: boundary-api
    type: vpc
    name: API Layer
    color: "#f97316"
    children:
      - apigw-rest
      - lambda-auth
      - lambda-api
      - lambda-worker
    _position: {x: 320, y: 100}
    _size: {width: 420, height: 340}
  - id: boundary-data
    type: subnet
    name: Data / Storage
    color: "#6366f1"
    children:
      - dynamodb-main
      - s3-uploads
      - sqs-queue
      - sns-topic
    _position: {x: 780, y: 100}
    _size: {width: 300, height: 340}

infrastructure:
  - id: cdn-cloudfront
    type: gateway
    name: CloudFront
    technology: AWS CloudFront
    _position: {x: 40, y: 40}
    _boundary: boundary-cdn
    connections:
      - target: s3-static
        label: Static Assets
      - target: apigw-rest
        label: API Proxy
  - id: s3-static
    type: storage
    name: S3 Static
    technology: AWS S3
    _position: {x: 40, y: 140}
    _boundary: boundary-cdn
  - id: apigw-rest
    type: gateway
    name: API Gateway
    technology: AWS API Gateway
    _position: {x: 40, y: 40}
    _boundary: boundary-api
    connections:
      - target: lambda-auth
        label: Authorizer
      - target: lambda-api
        label: Integration
  - id: lambda-auth
    type: service
    name: Auth Lambda
    technology: Node.js 20
    _position: {x: 220, y: 40}
    _boundary: boundary-api
  - id: lambda-api
    type: service
    name: API Lambda
    technology: Python 3.12
    _position: {x: 40, y: 180}
    _boundary: boundary-api
    connections:
      - target: dynamodb-main
        label: SDK
      - target: s3-uploads
        label: SDK
      - target: sqs-queue
        label: Publish
  - id: lambda-worker
    type: service
    name: Worker Lambda
    technology: Python 3.12
    _position: {x: 220, y: 180}
    _boundary: boundary-api
    connections:
      - target: sqs-queue
        label: Trigger
        direction: backward
      - target: dynamodb-main
        label: SDK
      - target: sns-topic
        label: Publish
  - id: dynamodb-main
    type: database
    name: DynamoDB
    technology: AWS DynamoDB
    _position: {x: 40, y: 40}
    _boundary: boundary-data
  - id: s3-uploads
    type: storage
    name: S3 Uploads
    technology: AWS S3
    _position: {x: 160, y: 40}
    _boundary: boundary-data
  - id: sqs-queue
    type: queue
    name: SQS Queue
    technology: AWS SQS
    _position: {x: 40, y: 160}
    _boundary: boundary-data
  - id: sns-topic
    type: queue
    name: SNS Topic
    technology: AWS SNS
    _position: {x: 160, y: 160}
    _boundary: boundary-data

_system_info_position: {x: 20, y: 20}
`,
  },
];
