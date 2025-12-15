import streamlit as st
import requests

def get_public_ip():
    """Получить публичный IP-адрес"""
    try:
        # Используем различные сервисы
        services = [
            'https://api.ipify.org',
            'https://ident.me',
            'https://checkip.amazonaws.com'
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue
        return "Не удалось получить публичный IP"
    except Exception as e:
        return f"Ошибка: {e}"

# Если requests не установлен, можно установить: pip install requests
st.write(f"Публичный IP: {get_public_ip()}")