---
title: House Price API
emoji: 🏠
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# 🏠 House Price Predictor API

A FastAPI service that predicts house prices using a PyTorch linear regression model.

## Features
- Predicts house prices based on size, bedrooms, and age
- Auto-generated interactive API docs
- Built-in input validation with Pydantic
- Containerized with Docker

## Endpoints
- `GET /` — Health check
- `GET /docs` — Interactive Swagger UI
- `POST /predict` — Predict a house price

## Example Usage

```bash
