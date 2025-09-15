# farm_gaurd_3P ( backend )

## file Structure :
backend/
├── .env.example            # Example environment variables
├── .gitignore             # Git ignore file
├── app/                   # Main application package
│   ├── _init_.py       # App initialization and configuration
│   ├── models/           # Database models
│   │   └── models.py     # All database models (User, Disease, etc.)
│   ├── routes/           # API routes/endpoints
│   │   ├── auth.py       # Authentication routes
│   │   ├── compliance.py # Compliance tracking routes
│   │   ├── disease.py    # Disease classification routes
│   │   ├── emergency.py  # Emergency response routes
│   │   ├── network.py    # Farmer network routes
│   │   └── users.py      # User management routes
│   ├── services/         # External services integration
│   │   └── firebase_service.py  # Firebase authentication service
│   └── utils/            # Utility functions and helpers
│       └── decorators.py # Role-based access control decorators
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
└── run.py               # Application entry point
