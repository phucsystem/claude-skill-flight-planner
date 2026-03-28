# Travel Optimization Engine

> Bộ 8 AI Skills tự động hóa toàn bộ quy trình tối ưu chi phí vé máy bay.
> Tiết kiệm 30-66% cho cá nhân/gia đình, 10-15% cho doanh nghiệp.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 8](https://img.shields.io/badge/Skills-8-blue.svg)](#8-skills)
[![Platform: Antigravity](https://img.shields.io/badge/Platform-Antigravity-purple.svg)](https://zalo.me/g/igkywu632)

## Quick Start

### Installation

```bash
# Clone vào thư mục skills của bạn
git clone https://github.com/dotanminh/travel-optimization-engine.git

# Di chuyển vào thư mục agent skills
# Windows:
move travel-optimization-engine .agents\skill\

# macOS/Linux:
mv travel-optimization-engine .agents/skill/
```

### Usage

Chỉ cần nói với AI:

```
"Tôi muốn bay HAN → SFO, 2 người lớn + 1 trẻ em, 
bay khoảng giữa tháng 6/2026, linh hoạt ±1 tuần"
```

AI sẽ tự động kích hoạt bộ skill phù hợp.

## 8 Skills

| # | Skill | Mô tả | Khi nào dùng |
|---|-------|-------|-------------|
| 1 | **date-optimization** | Phân tích giá theo ngày, chỗ rẻ nhất | Linh hoạt ngày bay |
| 2 | **flight-search** | Tìm vé từ nhiều nguồn + virtual interlining | Mọi lần tìm vé |
| 3 | **fee-analysis** | Bóc tách phí ẩn, tính tổng thực trả | Khi so sánh hãng LCC vs FSC |
| 4 | **route-optimization** | Tìm route rẻ hơn qua hub trung chuyển | Route quốc tế dài |
| 5 | **deals-verification** | Tìm mã giảm giá, deal từ hãng + ngân hàng | Mọi lần booking |
| 6 | **flexibility-analysis** | Phân tích rủi ro vé non-refundable | Lịch trình chưa chắc |
| 7 | **negotiation-email** | Soạn email thương lượng giá doanh nghiệp | Doanh nghiệp 50+ chuyến/năm |
| 8 | **hidden-city-strategy** | Phân tích hidden city (có risk disclaimer) | Nâng cao, chỉ khi được hỏi |

## Architecture

```
travel-optimization-engine/
├── SKILL.md                          # Orchestrator chính
├── README.md                         # File này
├── LICENSE                           # MIT License
├── CHANGELOG.md                      # Lịch sử thay đổi
├── .gitignore                        # Chặn API keys
├── scripts/
│   ├── kiwi_client.py                # Kiwi API client
│   ├── kiwi_tequila.py               # Kiwi Tequila wrapper
│   ├── amadeus_client.py             # Amadeus API client
│   ├── normalize.py                  # Price normalization
│   └── config.py                     # Configuration
├── assets/
│   ├── flow-diagram.html             # Interactive workflow diagram
│   └── report-template.md            # Template báo cáo cuối
├── references/
│   ├── glossary.md                   # Từ điển thuật ngữ hàng không
│   ├── airport-codes.md              # Hub + IATA codes + alliances
│   ├── amadeus-api.md                # Amadeus API reference
│   ├── kiwi-api.md                   # Kiwi API reference
│   └── user-profile-schema.md        # Schema thông tin hành khách
└── skills/
    ├── date-optimization/
    │   ├── SKILL.md
    │   └── references/pricing-patterns.md
    ├── flight-search/
    │   ├── SKILL.md
    │   └── references/
    │       ├── virtual-interlining.md
    │       └── api-integration.md
    ├── fee-analysis/
    │   ├── SKILL.md
    │   └── references/
    │       ├── airline-fee-matrix.md
    │       └── avoidance-strategies.md
    ├── route-optimization/
    │   ├── SKILL.md
    │   └── references/hub-analysis.md
    ├── deals-verification/
    │   ├── SKILL.md
    │   └── references/deal-sources.md
    ├── flexibility-analysis/
    │   ├── SKILL.md
    │   └── references/fare-class-rules.md
    ├── negotiation-email/
    │   └── SKILL.md
    └── hidden-city-strategy/
        ├── SKILL.md
        └── references/
            ├── enforcement-levels.md
            └── eligibility-check.md
```

## 2 Chế Độ Hoạt Động

### AI-Knowledge Mode (Không cần API)
- Sử dụng kiến thức AI về giá vé, trend, airline policies
- Đủ tốt cho phần lớn use cases
- Không cần cài đặt gì thêm

### API-Enhanced Mode (Real-time data)
- Kết nối Kiwi Tequila API cho dữ liệu giá vé thời gian thực
- Hỗ trợ virtual interlining (ghép vé nhiều hãng)
- Setup:
  ```bash
  pip install requests
  
  # Windows PowerShell:
  $env:KIWI_API_KEY="your_key_here"
  
  # macOS/Linux:
  export KIWI_API_KEY="your_key_here"
  ```
- Đăng ký API key miễn phí tại: https://tequila.kiwi.com/

## Workflow

```
Phase 1: Thu thập thông tin - Hỏi route, ngày, số người, preferences
Phase 2: Tìm kiếm        - Chạy date-optimization + flight-search song song  
Phase 3: Phân tích        - fee-analysis + route-optimization + deals-verification
Phase 4: Đánh giá         - flexibility-analysis (nếu có nhiều lựa chọn)
Phase 5: Xuất báo cáo     - Bảng so sánh cuối + recommendation
```

## Ví Dụ Output

```
╔══════════════════════════════════════════════════╗
║  TRAVEL OPTIMIZATION REPORT                      ║
║  HAN → SFO, 2A+1C, Jun 15-25, 2026             ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  BEST OPTION: Korean Air via ICN                 ║
║  True Total: $2,115 ($705/person)                ║
║  Saved: $885 vs booking direct (-30%)            ║
║                                                  ║
║  Key Savings Breakdown:                          ║
║  - Date shift Tue-Wed:        -$240              ║
║  - Hub routing via ICN:       -$345              ║
║  - Techcombank card:          -$120              ║
║  - Deal "KE Global Sale":    -$180               ║
║                                                  ║
║  Flexibility Score: 65/100 (Flex Economy)        ║
║  Risk: Low (schedule 90% certain)                ║
╚══════════════════════════════════════════════════╝
```

## Doanh Nghiệp

Skill 7 (negotiation-email) dành riêng cho doanh nghiệp:
- Soạn email cho đội Corporate Sales của hãng bay
- Đính kèm dữ liệu volume, route concentration, competitor pricing
- Template follow-up + talking points nếu hãng gọi lại

## Safety & Ethics

- **Hidden city** (Skill 8): Yêu cầu consent rõ ràng + eligibility check + full risk disclosure
- **Virtual interlining**: Cảnh báo rõ rủi ro tự kết nối (missed connection, không bảo hiểm delay)
- **Deal verification**: Mọi deal đều có nhãn confidence (HIGH/MEDIUM/LOW/EXPIRED)
- **Negotiation**: Không bao giờ tiết lộ giá tối đa của khách trong email

## Live Demo

Xem interactive workflow diagram: [travel-optimization-flow.vercel.app](https://travel-optimization-flow.vercel.app)

## Contributing

Issues và Pull Requests luôn được chào đón! Xem [CHANGELOG.md](CHANGELOG.md) để theo dõi lịch sử thay đổi.

## Credits

Built by [Minh Đỗ](https://zalo.me/g/igkywu632) with Antigravity Skill Architecture Standards.
API data powered by [Kiwi Tequila](https://tequila.kiwi.com/).

## License

[MIT](LICENSE)
