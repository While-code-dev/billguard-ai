# 🧾 BillGuard

### AI-Powered Bill Auditing & Charge Detection System

> **Know exactly what you're paying for.**

BillGuard is an AI-powered bill auditing application that analyzes bill images, extracts purchased items, taxes, discounts, and additional charges, and verifies the mathematical accuracy of the final bill.

It combines **AI-powered document understanding** with **deterministic Python-based verification** to help users identify billing discrepancies and understand exactly what they are being charged for.

---

## 🚀 Live Demo

🌐 **Live Application:**  
https://billguard-ai-gzbr4p8pjqbjgk8fsyv9fv.streamlit.app/

💻 **GitHub Repository:**  
https://github.com/While-code-dev/billguard-ai

---

## 🎯 Problem

Bills often contain multiple items, taxes, service charges, packaging fees, delivery charges, surcharges, and other additional amounts.

Manually checking whether every calculation is correct can be time-consuming and difficult.

Some charges may also be buried among the many lines of a bill, making it difficult for customers to understand exactly what they are paying for.

### Common problems include:

- Incorrect item calculations
- Quantity × unit-price mismatches
- Incorrect totals
- Unexpected additional charges
- Service or packaging fees
- Delivery or convenience charges
- Tax calculation confusion
- Difficulty understanding complex bills

---

## 💡 Solution

BillGuard allows users to simply upload a photo of their bill.

The system then:

1. 📷 Reads the bill using AI
2. 🤖 Extracts billing information
3. 🛒 Separates purchased items from taxes and additional charges
4. 🧮 Recalculates item totals using Python
5. 🔍 Detects mathematical discrepancies
6. ⚠️ Highlights additional charges
7. 📊 Compares the calculated total with the reported bill total
8. ✅ Provides a clear final verification

---

## ✨ Key Features

### 📷 AI Bill Extraction

Upload a bill image and BillGuard automatically extracts:

- Merchant name
- Bill type
- Purchased items
- Quantities
- Unit prices
- Item totals
- Taxes
- Discounts
- Additional charges
- Grand total

---

### 🛒 Item-Level Verification

For every item, BillGuard calculates:

```text
Quantity × Unit Price
