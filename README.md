# README #

VMS-Snapshots
![Image description](vms-snapshots/login.png)
![Image description](vms-snapshots/active-visitor.png)
![Image description](vms-snapshots/inactive-visitor.png)
![Image description](vms-snapshots/visitor-reg1.png)
![Image description](vms-snapshots/visitor-reg2.png)
![Image description](vms-snapshots/visitor-reg-3.png)
![Image description](vms-snapshots/gatepass.png)
![Image description](vms-snapshots/orgnisation.png)
![Image description](vms-snapshots/unit.png)
![Image description](vms-snapshots/gate.png)
![Image description](vms-snapshots/department.png)
![Image description](vms-snapshots/employee.png)
![Image description](vms-snapshots/report.png)
![Image description](vms-snapshots/analytics1.png)
![Image description](vms-snapshots/analytics2.png)
![Image description](vms-snapshots/QR.png)
![Image description](vms-snapshots/self-reg-1.png)
![Image description](vms-snapshots/self-reg-2.png)
![Image description](vms-snapshots/self-reg-3.png)
![Image description](vms-snapshots/self-reg-gatepass.png)



### Objective

The primary goal of the VMS is to provide real-time tracking of visitors, including their check-in and check-out times, to enhance security and efficiency within organizations.

### Workflow

**Use Cases:**

1. **Self-Registration:** Visitors can scan a QR code provided at designated gates to access a registration form. Upon completion, they receive an email notification with their registration details.
2. **Receptionist Registration:** Receptionists can manually register visitors through a centralized dashboard, capturing essential information.

**Data Points:**

- Name
- Address
- Mobile number
- Photo
- Number of accompanying persons
- Vehicle information
- Meeting purpose
- Entry gate
- Check-in time

**Notifications:**

Upon successful registration, the relevant individual receives an email notification containing the visitor's name, check-in time, purpose of visit, and accompanying persons.

### Key Features

* **Customization:** The VMS is highly configurable to meet the specific needs of different organizations.
* **Organizational Structure:** The system supports hierarchical structures, allowing for separation by organization, unit, and gate.
* **Real-Time Tracking:** Provides real-time monitoring of visitor activity, including check-in and check-out times.
* **Comprehensive Reporting:** Generates detailed reports in both tabular and graphical formats, allowing for easy analysis and tracking.
* **Date Range Filtering:** Enables users to filter reports based on specific date ranges.
* **Excel Export:** Provides the option to export data to Excel for further analysis or storage.

### Additional Considerations

* **Security:** Implement robust security measures to protect sensitive visitor information.
* **Integration:** Explore integration possibilities with existing systems, such as access control or security cameras.
* **User Experience:** Design an intuitive and user-friendly interface for both visitors and receptionists.

By implementing these features and considerations, the VMS can effectively manage visitor traffic, enhance security, and improve overall organizational efficiency.

### To generate dummy data ###
* python manage.py generate_data


### To configure the Hasura ###

## Overview

This project uses Hasura to provide instant GraphQL APIs for our PostgreSQL database. Hasura simplifies data access and management, offering features like real-time subscriptions, role-based access control, and seamless integration with custom business logic.

## Features

- **GraphQL API**: Automatically generated GraphQL schema based on the PostgreSQL database schema.
- **Real-time Subscriptions**: Real-time updates for queries via GraphQL subscriptions.
- **Authentication & Authorization**: Built-in support for JWT and role-based access control.
- **Event Triggers**: Invoke webhooks or serverless functions on database events.
- **Remote Schemas**: Integrate remote GraphQL schemas with the Hasura schema.
- **Migrations**: Manage database schema and track changes with migrations.

## Getting Started

## Prerequisites

- Docker
- PostgreSQL
- Node.js and npm (for Hasura CLI)

### setup 
### settings.py
```
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
        'NAME': os.environ.get('POSTGRES_DB', 'visitor_db'),
        'USER': os.environ.get('POSTGRES_USER', 'visitor_admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'admin123'),

    
    }
}
```

## docker-compose.yaml
```
version: "3"

services:
  db:
    image: mdillon/postgis
    container_name: visitor_database
    ports:
      - "5432:5432"
    volumes:
      - visitor_db:/var/lib/postgresql/data
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
      - POSTGRES_DB=visitor_db
      - POSTGRES_USER=visitor_admin
      - POSTGRES_PASSWORD=admin123
    networks:
      - db_network

  graphql-engine:
    image: hasura/graphql-engine:v2.38.0
    ports:
      - "8080:8080"
    depends_on:
      - "db"
    environment:
      HASURA_GRAPHQL_DATABASE_URL: postgres://visitor_admin:admin123@db:5432/visitor_db
      ## enable the console served by server
      HASURA_GRAPHQL_ENABLE_CONSOLE: "true" # set to "false" to disable console
      ## enable debugging mode. It is recommended to disable this in production
      HASURA_GRAPHQL_DEV_MODE: "true"
      HASURA_GRAPHQL_ENABLED_LOG_TYPES: startup, http-log, webhook-log, websocket-log, query-log
      ## uncomment next line to set an admin secret
      HASURA_GRAPHQL_ADMIN_SECRET: visitor_db
      HASURA_GRAPHQL_JWT_SECRET: '{"type":"HS256","key":"F8fmcyKmgcm8lZSIZoCbxCTPCW21Ej0C","claims_namespace":"user_claims","claims_format":"json"}'
    restart: always
    networks:
      - db_network

  graphql-data-connector:
    image: hasura/graphql-data-connector:v2.38.0
    container_name: data-connector-agent-1
    ports:
      - "8081:8081"
    depends_on:
      - db
    networks:
      - db_network
      
networks:
  db_network:
    driver: bridge

volumes:
  visitor_db:
```

### Run the following command to start the services:
- docker-compose up -d

### Set Up Hasura CLI
- npm install -g Hasura-cli

### Initialize Hasura Project
- hasura init vms-hasura --endpoint http://localhost:8080 --admin-secret visitor_db

### Apply Migrations and Metadata
- cd vms-hasura
- hasura migrate apply --endpoint http://localhost:8080 --admin-secret visitor_db
- hasura metadata apply --endpoint http://localhost:8080 --admin-secret visitor_db

### Start Hasura Console
- hasura console --endpoint http://localhost:8080 --admin-secret visitor_db
