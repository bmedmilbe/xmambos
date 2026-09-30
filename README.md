# 🏛️ CamaraMZ — Multi-Application Django Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.15-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)
[![Pipenv](https://img.shields.io/badge/Dependency%20Management-Pipenv-yellow.svg)](https://pipenv.pypa.io/)

CamaraMZ is a Django-based monorepo that brings together four applications within a shared backend infrastructure. The platform uses a single shared database and an NGINX reverse-proxy gateway to route incoming requests to the appropriate applications.

Selected applications use Django Tenants to support multi-tenant functionality, while others operate without a multi-tenant architecture where it is not required.

## 📋 Project Overview

The platform consists of four applications:

### 1. CMS — Content Management System

A content management application that enables website administrators to manage and maintain website content.

### 2. Remittance

An application for managing remittance instructions and related data for transfers from abroad to São Tomé and Príncipe.

The application supports the management of remittance information but does not directly execute money transfers.

### 3. Tour — Tourism Marketplace

A tourism marketplace focused on São Tomé and Príncipe, designed to promote and make tourism services and experiences available.

### 4. Certificate — Municipal Certificate Management

An application for managing and issuing official certificates for Câmara Distrital de Mé-Zóchi, São Tomé and Príncipe.

The application uses Django Tenants to support multiple district councils within the same application. It is currently implemented for Câmara Distrital de Mé-Zóchi, with the architecture allowing other councils to use the application.

## 🏗️ Architecture

The platform follows a multi-application architecture within a single repository.

- **Four Django applications:** CMS, Remittance, Tour and Certificate.
- **Shared database:** All four applications use a single database.
- **Multi-tenancy:** Django Tenants is used by each applications.
- **NGINX Gateway:** Acts as the reverse proxy and single entry point for incoming requests.
- **Request routing:** NGINX forwards incoming requests to the appropriate application.
- **Application access:** Users access the platform through the gateway rather than directly accessing the individual applications.

### Request Flow

```text
                    Users / Clients
                           |
                           v
                   NGINX Gateway
                  (Reverse Proxy)
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
           CMS        Remittance        Tour
             |
             |          Certificate
             |             ^
             +-------------+
                           |
                           v
                  Shared Database
```

The diagram is a conceptual overview. The actual NGINX routing rules determine how requests are directed to each application, and all four applications connect to the shared database.

### Multi-Tenant Architecture

Multi-tenancy is implemented selectively rather than applied across the entire platform.

The Certificate application uses Django Tenants to support multiple district councils. Other applications use the architecture appropriate to their requirements.

## 🛠️ Technology Stack

| Technology            | Purpose                                             |
| --------------------- | --------------------------------------------------- |
| Python                | Backend development                                 |
| Django                | Application framework                               |
| Django REST Framework | REST API development                                |
| PostgreSQL            | Shared relational database                          |
| Django Tenants        | Multi-tenant functionality in selected applications |
| NGINX                 | Reverse proxy and request routing                   |
| Pipenv                | Python dependency management                        |

## 📁 Repository Structure

The repository contains four Django applications within a single codebase:

- CMS
- Remittance
- Tour
- Certificate

Each application provides a distinct area of functionality while sharing the platform's database and infrastructure.

## 🚀 Getting Started

To run the project locally:

1. Clone the repository.
2. Install the project dependencies using Pipenv.
3. Configure the required environment variables.
4. Configure the shared database connection.
5. Apply the database migrations.
6. Start the Django applications.
7. Configure and start NGINX as the gateway.

Refer to the project's configuration files and deployment setup for the exact commands and environment variables.

## 👨‍💻 Author

**Edmilbe Ramos** — Python Backend Developer

- [GitHub](https://github.com/bmedmilbe)
- [LinkedIn](https://www.linkedin.com/in/edmilbe-ramos/)
- Email: bm.edmilbe@gmail.com
