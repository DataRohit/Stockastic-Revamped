# Stockastic Revamped 📈

A comprehensive stock monitoring platform providing real-time investment insights with secure authentication. Track your favorite stocks and visualize performance through interactive Plotly graphs.

## ✨ Features

- **Real-time Data Streaming**: Utilizing WebSockets for live market updates
- **Comprehensive Market Coverage**: 
  - Indices tracking
  - Top gainers and losers
  - BSE and NSE equity stocks
- **Interactive Visualization**: Plotly-powered charts for detailed market analysis
- **Personalized Dashboard**: Bookmark/unbookmark stocks and indices to track favorites
- **Dual Exchange Support**: Toggle between BSE and NSE for equity stocks
- **Multiple Index Categories**: Various index options sourced from NSE Python and BSE website

## 🛠️ Technology Stack

### Core
- Django 4.2.17
- Python 3.13.1
- WebSockets (websockets 14.1)
- Plotly 5.24.1
- Redis 5.2.1

### Infrastructure
- PostgreSQL (Database)
- MinIO (Storage)
- Nginx (Web Server)

### Data Sources
- NSE Python (2.94)
- yfinance (0.2.51)

## 📊 Data Visualization

- Interactive Plotly charts for each index/equity stock
- Detailed view combining charts with comprehensive stock information
- Real-time data updates through WebSocket connections

## 📝 Requirements

A comprehensive list of Python dependencies is maintained in `requirements.txt`. Key packages include:

- Django and related packages (django-cors-headers, django-redis, etc.)
- Data processing tools (pandas, numpy)
- Visualization libraries (plotly)
- WebSocket support
- Database connectors
- Development and testing utilities

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the `license` file for details.

## 🙏 Acknowledgments

- NSE Python library contributors
- yfinance maintainers
- Django community
- All contributors who have helped shape this project
