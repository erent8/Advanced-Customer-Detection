Advanced_Customer_Detection/
│
├── database/                      # Database operations
│   ├── customer_data.db          # Main SQLite database
│   └── backup/                   # Database backups
│       └── daily/
│
├── logs/                         # Application logs
│   ├── app.log                   # General application logs
│   ├── error.log                # Error logs
│   └── performance.log          # Performance metrics
│
├── reports/                      # Reporting system
│   ├── analytics/               # Analytics reports
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── monthly/
│   ├── exports/                # Exported reports
│   │   ├── pdf/
│   │   └── excel/
│   └── visualizations/         # Generated visualizations
│       ├── heatmaps/
│       ├── trends/
│       └── density/
│
├── src/                         # Source code
│   ├── __init__.py
│   ├── analytics.py            # Analytics module
│   ├── api.py                 # REST API implementation
│   ├── camera.py              # Camera handling
│   ├── dashboard.py           # Web dashboard
│   ├── database.py            # Database operations
│   ├── detector.py            # Detection algorithms
│   ├── logger.py              # Logging system
│   ├── models.py              # Database models
│   ├── monitoring.py          # Performance monitoring
│   ├── notification.py        # Notification system
│   ├── security.py            # Security features
│   ├── utils.py               # Utility functions
│   └── visualization.py       # Data visualization
│
├── static/                      # Static files for web
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                   # HTML templates
│   ├── dashboard/
│   ├── reports/
│   └── analytics/
│
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_analytics.py
│   ├── test_api.py
│   ├── test_camera.py
│   ├── test_dashboard.py
│   ├── test_database.py
│   ├── test_detector.py
│   └── test_monitoring.py
│
├── config/                     # Configuration files
│   ├── camera_config.yaml
│   ├── dashboard_config.yaml
│   └── notification_config.yaml
│
├── scripts/                    # Utility scripts
│   ├── setup_camera.py
│   ├── benchmark.py
│   ├── backup.py
│   └── system_check.py
│
├── .env                        # Environment variables
├── .gitignore                 # Git ignore file
├── LICENSE                    # Open Source Project
├── README.md                  # Project documentation (Turkish)
├── README_EN.md              # Project documentation (English)
├── requirements.txt           # Python dependencies
└── run_dashboard.py          # Main application entry