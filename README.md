# Mirisa API Server
Unid-thon Hackathon에서 만들어진 API 서버입니다.
1인 가구의 계획적인 지출과 생필품을 잊지 않고 제 때 살 수 있도록 유도하는 목적으로 만들어진 Mirisa 서비스의 백엔드 API 서버입니다.

## Features
- 회원가입 시 사용자 자동 생성
- 유저 생성 시 유저의 생필품 리스트를 자동으로 생성
- 유저가 물품을 구매 시 추가 할 수 있는 addone, addall 기능
- 유저가 가지고 있는 생필품의 리스트를 받을 수 있는 기능
- 유저가 가진 생필품을 사용하고 기록할 수 있는 기능
- 유저가 물건을 산 가격을 추적하여 다음 해당 물건의 예상 금액을 유추하는 기능
- 유저가 물건을 소비하는 주기를 추적하여 다음 해당 물건의 예상 소모일을 유추하는 기능

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Uni-dthon/mirisa-api-server.git
    cd mirisa-api-server
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv myvenv
    source myvenv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Environment Variables**: .env at root position in repository
    Use MYSQL server
   ```plaintext
    DB_HOST='Database server IP'
    DB_USER='DB_USER'
    DB_PASSWORD='DB_PASSWORD'
    ```

5. **Database Setup**: This repository use other ec2 instance for mysql or RDS service in AWS
    ```bash
    sudo apt update
    sudo apt install mysql-server -y
    sudo mysql_secure_installation -> type 'y' in all configuration
    sudo systemctl start mysql
    sudo systemctl enable mysql
    sudo mysql
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'DB_PASSWORD'; -> your_password should be replaced with your password
    GRANT ALL PRIVILEGES ON your_database.* TO 'DB_USER'@'%'; -> DB_USER should be replaced with your database username
    GRANT ALL PRIVILEGES ON *.* TO 'DB_USER'@'%'; -> DB_USER should be replaced with your database username
    FLUSH PRIVILEGES;
    exit
    sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
    ```
    Replace some lines with this one
    ```bash
    bind-address = 0.0.0.0
    mysqlx-bind-address = 0.0.0.0
    ```
    Restart mysql service
    ```bash
    sudo systemctl restart mysql
    ```

6. **Run Server**:
    ```
    cd ~/mirisa-api-server
    python3 main.py
    ```

## API Documentation: Swagger
    Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser for API documentation.

## Project Structure
    ```bash
    ├── .github/workflows/
    │   └── cd.yml                 # CI/CD workflow configuration for GitHub Actions
    ├── Data/                      # Data-related modules
    │   ├── item.py                # Item data handling with pydantic
    │   └── user.py                # User data handling with pydantic
    ├── Database/                  # Database connection and models
    │   ├── database.py            # Database connection and setup
    │   └── models.py              # Database models definition
    ├── Router/                    # API route handlers
    │   ├── item.py                # Routes for item-related operations
    │   ├── login.py               # Routes for user login operations
    │   └── price.py               # Routes for price-related operations
    ├── Service/                   # Business logic and services
    │   ├── consume_service.py     # Service for consumption-related logic
    │   ├── embedding_service.py   # Service for embedding-related logic
    │   ├── item_service.py        # Service for item-related logic
    │   ├── purchase_service.py    # Service for purchase-related logic
    │   ├── user_service.py        # Service for user-related logic
    │   └── useritem_service.py    # Service for user-item relationship logic
    ├── .gitignore                 # Git ignore file for excluding specific files/folders
    ├── main.py                    # Main entry point of the application
    ├── README.md                  # Project documentation
    └── requirements.txt           # List of dependencies
    ```

## Contributors
<a href="https://github.com/rocknroll17">
  <img src="https://github.com/rocknroll17.png" width="50" height="50" alt="rocknroll17">
</a>
<a href="https://github.com/jingooo5">
  <img src="https://github.com/jingooo5.png" width="50" height="50" alt="jingooo5">
</a>