import os
import json
import re
import base64
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY missing")
    st.stop()

client = genai.Client(api_key=API_KEY)

PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-2.5-flash-lite"

st.set_page_config(
    page_title="BillGuard",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 5% 10%,
                rgba(251,146,60,.13),
                transparent 22%
            ),
            radial-gradient(
                circle at 95% 20%,
                rgba(167,139,250,.14),
                transparent 23%
            ),
            radial-gradient(
                circle at 80% 90%,
                rgba(45,212,191,.13),
                transparent 25%
            ),
            #fff8ee;

        color: #172033;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 0;
        padding-bottom: 5rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    .hero {
        min-height: 600px;

        display: flex;
        align-items: center;
        justify-content: center;

        text-align: center;

        background:
            radial-gradient(
                circle at 12% 20%,
                rgba(99,102,241,.38),
                transparent 28%
            ),
            radial-gradient(
                circle at 88% 18%,
                rgba(245,158,11,.32),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(20,184,166,.25),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #20255f 0%,
                #4c3a8c 52%,
                #7c3f68 100%
            );

        border-radius: 0 0 46px 46px;

        padding: 75px 25px;

        margin-bottom: 70px;

        color: white;

        box-shadow:
            0 25px 70px rgba(76,58,140,.20);
    }

    .hero-content {
        max-width: 900px;
        margin: auto;
    }

    .logo {
        width: 82px;
        height: 82px;

        border-radius: 25px;

        background:
            linear-gradient(
                135deg,
                #ffffff,
                #fff1c7
            );

        border: 1px solid rgba(255,255,255,.8);

        display: flex;

        align-items: center;
        justify-content: center;

        font-size: 42px;

        margin: 0 auto 27px auto;

        box-shadow:
            0 14px 35px rgba(0,0,0,.18);
    }

    .hero h1 {
        font-size: 68px;
        font-weight: 800;
        letter-spacing: -4px;
        margin: 0;
        color: #ffffff;
    }

    .hero h2 {
        font-size: 27px;
        font-weight: 500;
        color: #f1eaff;
        margin: 17px 0;
    }

    .hero p {
        font-size: 18px;
        line-height: 1.8;
        color: #f7f3ff;
        max-width: 730px;
        margin: 22px auto;
    }

    .section {
        padding: 20px 0 65px 0;
    }

    .section-title {
        text-align: center;
        font-size: 36px;
        font-weight: 800;
        color: #29213d;
        margin-bottom: 12px;
        letter-spacing: -1px;
    }

    .section-subtitle {
        text-align: center;
        color: #756b7d;
        font-size: 16px;
        margin-bottom: 35px;
    }

    .feature {
        background: #fffdf9;
        border-radius: 24px;
        padding: 30px;
        min-height: 215px;

        box-shadow:
            0 12px 35px rgba(101,76,45,.08);

        border: 1px solid #f0dfca;
    }

    .feature:nth-child(1) {
        border-top: 4px solid #6366f1;
    }

    .feature:nth-child(2) {
        border-top: 4px solid #f59e0b;
    }

    .feature:nth-child(3) {
        border-top: 4px solid #10b981;
    }

    .feature-icon {
        width: 58px;
        height: 58px;

        border-radius: 17px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 29px;

        margin-bottom: 18px;
    }

    .feature:nth-child(1) .feature-icon {
        background: #eeedff;
    }

    .feature:nth-child(2) .feature-icon {
        background: #fff2cf;
    }

    .feature:nth-child(3) .feature-icon {
        background: #dff8ed;
    }

    .feature h3 {
        color: #29213d;
        margin: 0 0 10px 0;
    }

    .feature p {
        color: #756b7d;
        line-height: 1.7;
        margin: 0;
    }

    .upload-section {
        background: #fffdf9;

        border: 1px solid #efdfca;

        border-radius: 28px;

        padding: 38px;

        box-shadow:
            0 15px 45px rgba(101,76,45,.09);
    }

    .result-header {
        background:
            linear-gradient(
                120deg,
                #28245f,
                #56419a 55%,
                #7b416f
            );

        color: white;

        border-radius: 26px;

        padding: 32px;

        margin: 35px 0;

        box-shadow:
            0 18px 45px rgba(76,58,140,.18);
    }

    .result-header h2 {
        margin: 0;
        font-size: 31px;
    }

    .result-header p {
        color: #eee8ff;
        margin: 8px 0 0 0;
    }

    .total-card {
        background: #fffdf9;

        border-radius: 21px;

        padding: 27px;

        text-align: center;

        min-height: 120px;

        border: 1px solid #efdfca;

        box-shadow:
            0 10px 30px rgba(101,76,45,.07);
    }

    .total-card .label {
        color: #817687;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: .5px;
    }

    .total-card .value {
        font-size: 30px;
        font-weight: 800;
        margin-top: 9px;
        color: #29213d;
    }

    .breakdown-header {
        background:
            linear-gradient(
                90deg,
                #34305d,
                #55437c
            );

        color: white;

        border-radius: 17px;

        padding: 18px 23px;

        margin-top: 25px;

        margin-bottom: 10px;

        font-weight: 700;

        box-shadow:
            0 8px 22px rgba(76,58,140,.13);
    }

    .item-card {
        background: #fffdf9;

        border: 1px solid #efdfca;

        border-radius: 17px;

        padding: 20px 23px;

        margin: 9px 0;

        box-shadow:
            0 6px 20px rgba(101,76,45,.05);
    }

    .item-card-warning {
        background:
            linear-gradient(
                90deg,
                #fff8e8,
                #fffdf9
            );

        border: 1px solid #f3c76b;

        border-left: 5px solid #f59e0b;
    }

    .item-name {
        font-size: 16px;
        font-weight: 700;
        color: #29213d;
    }

    .item-detail {
        font-size: 13px;
        color: #817687;
        margin-top: 5px;
    }

    .item-price {
        font-size: 17px;
        font-weight: 800;
        color: #29213d;
        text-align: right;
    }

    .charge-section {
        background:
            linear-gradient(
                135deg,
                #fff3d5,
                #fffaf0
            );

        border: 1px solid #f4c65f;

        border-radius: 24px;

        padding: 27px;

        margin-top: 30px;

        box-shadow:
            0 10px 30px rgba(245,158,11,.09);
    }

    .charge-title {
        color: #a45108;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .charge-card {
        background: #fffdf9;

        border: 1px solid #f4d58d;

        border-radius: 15px;

        padding: 18px 21px;

        margin: 10px 0;
    }

    .charge-name {
        color: #91460b;
        font-size: 16px;
        font-weight: 700;
    }

    .charge-amount {
        color: #e85d04;
        font-size: 18px;
        font-weight: 800;
        text-align: right;
    }

    .tax-section {
        background:
            linear-gradient(
                135deg,
                #efefff,
                #faf9ff
            );

        border: 1px solid #c9c6f7;

        border-radius: 24px;

        padding: 27px;

        margin-top: 30px;

        box-shadow:
            0 10px 30px rgba(79,70,229,.07);
    }

    .tax-title {
        color: #5146a8;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .tax-card {
        background: #fffdf9;

        border: 1px solid #d9d6f3;

        border-radius: 15px;

        padding: 18px 21px;

        margin: 10px 0;
    }

    .tax-name {
        color: #494092;
        font-size: 16px;
        font-weight: 700;
    }

    .tax-amount {
        color: #29213d;
        font-size: 17px;
        font-weight: 700;
        text-align: right;
    }

    .extra-card {
        background:
            linear-gradient(
                135deg,
                #fff0eb,
                #fffaf8
            );

        border: 1px solid #f3a898;

        border-left: 5px solid #ef4444;

        border-radius: 22px;

        padding: 30px;

        margin: 30px 0;

        box-shadow:
            0 10px 30px rgba(239,68,68,.07);
    }

    .extra-card h3 {
        color: #c2410c;
        margin-top: 0;
    }

    .extra-value {
        font-size: 38px;
        font-weight: 800;
        color: #dc2626;
    }

    .clean-card {
        background:
            linear-gradient(
                135deg,
                #e5f9ef,
                #f8fffb
            );

        border: 1px solid #8bd8b5;

        border-left: 5px solid #10b981;

        border-radius: 22px;

        padding: 30px;

        margin: 30px 0;

        box-shadow:
            0 10px 30px rgba(16,185,129,.07);
    }

    .clean-card h3 {
        color: #047857;
        margin-top: 0;
    }

    .verification-card {
        background:
            linear-gradient(
                135deg,
                #e5f9ef,
                #f8fffb
            );

        border: 1px solid #8bd8b5;

        border-radius: 20px;

        padding: 24px;

        color: #047857;

        font-size: 16px;

        margin-top: 20px;
    }

    .review-card {
        background:
            linear-gradient(
                135deg,
                #fff3d5,
                #fffaf0
            );

        border: 1px solid #f4c65f;

        border-radius: 20px;

        padding: 24px;

        color: #91460b;

        font-size: 16px;

        margin-top: 20px;
    }

    .stButton > button {
        border: none !important;

        border-radius: 14px !important;

        background:
            linear-gradient(
                90deg,
                #5146a8,
                #7c3aed,
                #e85d04
            ) !important;

        color: white !important;

        font-weight: 700 !important;

        font-size: 16px !important;

        padding: 14px !important;

        box-shadow:
            0 10px 25px rgba(81,70,168,.20) !important;

        transition:
            transform .2s ease,
            box-shadow .2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 14px 32px rgba(81,70,168,.28) !important;
    }

    [data-testid="stFileUploader"] {
        background:
            linear-gradient(
                135deg,
                #f4efff,
                #fffaf0
            );

        border: 2px dashed #a78bfa;

        border-radius: 20px;

        padding: 18px;

        color: #494092;
    }

    [data-testid="stFileUploader"] section {
        background: transparent !important;
    }

    .footer {
        text-align: center;

        color: #897c88;

        border-top: 1px solid #eadcca;

        padding-top: 28px;

        margin-top: 55px;

        font-weight: 500;
    }

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero h1 {
            font-size: 48px;
        }

        .hero h2 {
            font-size: 21px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)

st.html(
    """
    <div class="hero">
        <div class="hero-content">

            <div class="logo">🧾</div>

            <h1>BillGuard</h1>

            <h2>Know exactly what you're paying for.</h2>

            <p>
                BillGuard uses AI to read your bill, verify every calculation,
                identify additional charges and highlight amounts that need your attention.
            </p>

        </div>
    </div>
    """
)

st.html(
    """
    <div class="section">

        <div class="section-title">
            Your bill. Audited by AI.
        </div>

        <div class="section-subtitle">
            Upload a bill and BillGuard breaks it down for you.
        </div>

    </div>
    """
)

c1, c2, c3 = st.columns(3)

with c1:
    st.html(
        """
        <div class="feature">

            <div class="feature-icon">📷</div>

            <h3>1. Upload</h3>

            <p>
                Take a photo or upload an image of your bill.
            </p>

        </div>
        """
    )

with c2:
    st.html(
        """
        <div class="feature">

            <div class="feature-icon">🤖</div>

            <h3>2. AI Audits</h3>

            <p>
                BillGuard extracts items, prices, taxes and additional charges.
            </p>

        </div>
        """
    )

with c3:
    st.html(
        """
        <div class="feature">

            <div class="feature-icon">🔎</div>

            <h3>3. Find Issues</h3>

            <p>
                See additional charges and calculation differences clearly.
            </p>

        </div>
        """
    )

st.html(
    """
    <div class="section">

        <div class="section-title">
            Ready to check your bill?
        </div>

        <div class="section-subtitle">
            Upload your bill below and let BillGuard audit it.
        </div>

    </div>
    """
)

st.html(
    """
    <div class="upload-section">

        <div style="
            text-align:center;
            font-size:20px;
            font-weight:700;
            color:#5146a8;
            margin-bottom:12px;
        ">
            📄 Upload your bill
        </div>

        <div style="
            text-align:center;
            color:#817687;
            margin-bottom:20px;
        ">
            JPG, JPEG or PNG
        </div>

    </div>
    """
)

uploaded_file = st.file_uploader(
    "Upload your bill",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

if uploaded_file:

    original_image = Image.open(uploaded_file)

    image = original_image.copy()

    image.thumbnail((1600, 1600))

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=85,
        optimize=True
    )

    image_bytes = buffer.getvalue()

    mime_type = "image/jpeg"

    preview_left, preview_center, preview_right = st.columns(
        [1, 2, 1]
    )

    with preview_center:

        st.image(
            image,
            width=700
        )

    if st.button(
        "🔍 Audit My Bill",
        type="primary",
        use_container_width=True
    ):

        prompt = """
Analyze this bill image and return ONLY valid JSON.

Extract every monetary line and classify it into exactly these categories:

ITEMS:
Actual purchased products or services.

TAXES:
GST, CGST, SGST, IGST, VAT, cess, or other taxes.

ADDITIONAL_CHARGES:
Any non-item, non-tax charge such as gas charge, service charge,
packaging charge, delivery fee, handling fee, convenience fee,
platform fee, container charge, surcharge, fuel charge, processing fee,
or any other separately charged fee.

DISCOUNT:
Any discount shown on the bill.

Use this exact JSON structure:

{
  "merchant": "",
  "bill_type": "",
  "currency": "₹",
  "items": [
    {
      "name": "",
      "quantity": 1,
      "unit_price": 0,
      "total": 0
    }
  ],
  "taxes": [
    {
      "name": "",
      "amount": 0
    }
  ],
  "additional_charges": [
    {
      "name": "",
      "amount": 0
    }
  ],
  "discount": 0,
  "subtotal": 0,
  "grand_total": 0
}

Rules:
- Extract all visible monetary lines.
- Do not classify fees or charges as items.
- Do not classify taxes as additional charges.
- A line such as "Gas Charge Fixed 30" is an additional charge.
- Preserve names and amounts from the bill.
- Do not invent values.
- Use empty arrays when a category is absent.
"""

        with st.spinner(
            "BillGuard is auditing your bill..."
        ):

            image_b64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            models_to_try = [
                PRIMARY_MODEL,
                FALLBACK_MODEL
            ]

            bill = None
            last_error = None
            successful_model = None

            for model_name in models_to_try:

                try:

                    interaction = client.interactions.create(
                        model=model_name,
                        store=False,
                        input=[
                            {
                                "type": "image",
                                "mime_type": mime_type,
                                "data": image_b64
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    )

                    text = interaction.output_text.strip()

                    text = re.sub(
                        r"```json|```",
                        "",
                        text
                    ).strip()

                    bill = json.loads(text)

                    successful_model = model_name

                    break

                except Exception as e:

                    last_error = str(e)

                    if "429" not in last_error and "RESOURCE_EXHAUSTED" not in last_error:
                        break

            if bill is None:

                if last_error and (
                    "429" in last_error
                    or "RESOURCE_EXHAUSTED" in last_error
                    or "rate limit" in last_error.lower()
                    or "quota" in last_error.lower()
                ):

                    st.error(
                        "Gemini API quota is currently exhausted."
                    )

                    st.warning(
                        "Both BillGuard AI models are currently rate-limited. "
                        "Please wait for the quota to reset or use a Gemini API "
                        "project with available quota."
                    )

                    st.stop()

                else:

                    st.error(
                        "Unable to analyze the bill."
                    )

                    st.code(
                        last_error or "Unknown error"
                    )

                    st.stop()

        items = bill.get(
            "items",
            []
        )

        taxes_list = bill.get(
            "taxes",
            []
        )

        charges_list = bill.get(
            "additional_charges",
            []
        )

        calculated_items_total = 0

        item_errors = []

        for item in items:

            quantity = float(
                item.get(
                    "quantity",
                    0
                ) or 0
            )

            unit_price = float(
                item.get(
                    "unit_price",
                    0
                ) or 0
            )

            reported_total = float(
                item.get(
                    "total",
                    0
                ) or 0
            )

            calculated_item_total = (
                quantity * unit_price
            )

            calculated_items_total += calculated_item_total

            if abs(
                calculated_item_total - reported_total
            ) > 0.01:

                item_errors.append(
                    {
                        "name": item.get(
                            "name",
                            "Unknown"
                        ),
                        "reported": reported_total,
                        "calculated": calculated_item_total,
                        "difference":
                            reported_total - calculated_item_total
                    }
                )

        tax_total = sum(
            float(
                tax.get(
                    "amount",
                    0
                ) or 0
            )
            for tax in taxes_list
        )

        additional_charge_total = sum(
            float(
                charge.get(
                    "amount",
                    0
                ) or 0
            )
            for charge in charges_list
        )

        discount = float(
            bill.get(
                "discount",
                0
            ) or 0
        )

        grand_total = float(
            bill.get(
                "grand_total",
                0
            ) or 0
        )

        calculated_total = (
            calculated_items_total
            + tax_total
            + additional_charge_total
            - discount
        )

        total_difference = (
            grand_total - calculated_total
        )

        currency = bill.get(
            "currency",
            "₹"
        )

        st.html(
            """
            <div class="result-header">

                <h2>
                    🔍 Bill Audit Complete
                </h2>

                <p>
                    Your bill has been analyzed and verified.
                </p>

            </div>
            """
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.html(
                f"""
                <div class="total-card">

                    <div class="label">
                        BILL TOTAL
                    </div>

                    <div class="value">
                        {currency} {grand_total:,.2f}
                    </div>

                </div>
                """
            )

        with c2:

            st.html(
                f"""
                <div class="total-card">

                    <div class="label">
                        CALCULATED TOTAL
                    </div>

                    <div class="value">
                        {currency} {calculated_total:,.2f}
                    </div>

                </div>
                """
            )

        with c3:

            if additional_charge_total > 0:

                st.html(
                    f"""
                    <div class="total-card">

                        <div class="label">
                            ADDITIONAL CHARGES
                        </div>

                        <div class="value"
                             style="color:#e85d04;">

                            {currency}
                            {additional_charge_total:,.2f}

                        </div>

                    </div>
                    """
                )

            else:

                st.html(
                    """
                    <div class="total-card">

                        <div class="label">
                            ADDITIONAL CHARGES
                        </div>

                        <div class="value"
                             style="color:#059669;">

                            ₹ 0.00

                        </div>

                    </div>
                    """
                )

        st.html(
            """
            <div class="section-title"
                 style="margin-top:55px;">

                🧾 Bill Breakdown

            </div>
            """
        )

        st.html(
            """
            <div class="breakdown-header">
                🛒 Purchased Items
            </div>
            """
        )

        for item in items:

            name = str(
                item.get(
                    "name",
                    "Unknown"
                )
            )

            quantity = float(
                item.get(
                    "quantity",
                    0
                ) or 0
            )

            unit_price = float(
                item.get(
                    "unit_price",
                    0
                ) or 0
            )

            reported_total = float(
                item.get(
                    "total",
                    0
                ) or 0
            )

            calculated_item_total = (
                quantity * unit_price
            )

            difference = (
                reported_total
                - calculated_item_total
            )

            if difference > 0.01:

                st.html(
                    f"""
                    <div class="item-card item-card-warning">

                        <div class="item-name">
                            ⚠️ {name}
                        </div>

                        <div class="item-detail">
                            {quantity:g}
                            ×
                            {currency}
                            {unit_price:,.2f}
                        </div>

                        <div style="
                            text-align:right;
                            margin-top:-42px;
                        ">

                            <div class="item-price">
                                {currency}
                                {reported_total:,.2f}
                            </div>

                            <div style="
                                color:#dc2626;
                                font-size:12px;
                                font-weight:700;
                                margin-top:4px;
                            ">

                                +
                                {currency}
                                {difference:,.2f}
                                calculation difference

                            </div>

                        </div>

                    </div>
                    """
                )

            else:

                st.html(
                    f"""
                    <div class="item-card">

                        <div class="item-name">
                            {name}
                        </div>

                        <div class="item-detail">
                            {quantity:g}
                            ×
                            {currency}
                            {unit_price:,.2f}
                        </div>

                        <div style="
                            text-align:right;
                            margin-top:-42px;
                        ">

                            <div class="item-price">
                                {currency}
                                {reported_total:,.2f}
                            </div>

                        </div>

                    </div>
                    """
                )

        if charges_list:

            st.html(
                """
                <div class="charge-section">

                    <div class="charge-title">
                        ⚠️ Additional Charges Detected
                    </div>

                    <div style="
                        color:#91460b;
                        margin-bottom:15px;
                    ">

                        These amounts are separate from
                        the purchased items and taxes.
                        Review them before paying.

                    </div>
                """
            )

            for charge in charges_list:

                charge_name = str(
                    charge.get(
                        "name",
                        "Additional Charge"
                    )
                )

                charge_amount = float(
                    charge.get(
                        "amount",
                        0
                    ) or 0
                )

                st.html(
                    f"""
                    <div class="charge-card">

                        <div class="charge-name">
                            {charge_name}
                        </div>

                        <div style="
                            text-align:right;
                            margin-top:-24px;
                        ">

                            <div class="charge-amount">

                                {currency}
                                {charge_amount:,.2f}

                            </div>

                        </div>

                    </div>
                    """
                )

            st.html(
                f"""
                <div style="
                    border-top:1px solid #f4d58d;
                    margin-top:18px;
                    padding-top:18px;
                ">

                    <div style="
                        font-size:14px;
                        color:#91460b;
                        font-weight:700;
                    ">

                        TOTAL ADDITIONAL CHARGES

                    </div>

                    <div style="
                        font-size:30px;
                        font-weight:800;
                        color:#e85d04;
                        margin-top:5px;
                    ">

                        {currency}
                        {additional_charge_total:,.2f}

                    </div>

                </div>

                </div>
                """
            )

        if taxes_list:

            st.html(
                """
                <div class="tax-section">

                    <div class="tax-title">
                        🧾 Taxes
                    </div>
                """
            )

            for tax in taxes_list:

                tax_name = str(
                    tax.get(
                        "name",
                        "Tax"
                    )
                )

                tax_amount = float(
                    tax.get(
                        "amount",
                        0
                    ) or 0
                )

                st.html(
                    f"""
                    <div class="tax-card">

                        <div class="tax-name">
                            {tax_name}
                        </div>

                        <div style="
                            text-align:right;
                            margin-top:-23px;
                        ">

                            <div class="tax-amount">

                                {currency}
                                {tax_amount:,.2f}

                            </div>

                        </div>

                    </div>
                    """
                )

            st.html(
                f"""
                <div style="
                    border-top:1px solid #d9d6f3;
                    margin-top:18px;
                    padding-top:18px;
                ">

                    <div style="
                        font-size:14px;
                        color:#5146a8;
                        font-weight:700;
                    ">

                        TOTAL TAX

                    </div>

                    <div style="
                        font-size:26px;
                        font-weight:800;
                        color:#29213d;
                        margin-top:5px;
                    ">

                        {currency}
                        {tax_total:,.2f}

                    </div>

                </div>

                </div>
                """
            )

        if item_errors:

            positive_item_difference = sum(
                error["difference"]
                for error in item_errors
                if error["difference"] > 0
            )

            if positive_item_difference > 0:

                st.html(
                    f"""
                    <div class="extra-card">

                        <h3>
                            ⚠️ Item Calculation Difference
                        </h3>

                        <div class="extra-value">

                            {currency}
                            {positive_item_difference:,.2f}

                        </div>

                        <p style="color:#9a3412;">

                            One or more items were billed
                            for more than their quantity ×
                            unit price calculation.

                        </p>

                    </div>
                    """
                )

        if not charges_list and not item_errors:

            st.html(
                """
                <div class="clean-card">

                    <h3>
                        ✅ No Additional Charges Detected
                    </h3>

                    <p style="color:#047857;">

                        BillGuard did not identify any
                        non-item, non-tax charges on this bill.

                    </p>

                </div>
                """
            )

        st.html(
            """
            <div class="section-title">

                📊 Final Verification

            </div>
            """
        )

        if abs(total_difference) <= 0.01:

            if additional_charge_total > 0:

                st.html(
                    f"""
                    <div class="review-card">

                        <strong>
                            ⚠️ Bill total verified,
                            but additional charges were found.
                        </strong>

                        <br><br>

                        The bill mathematically adds up to

                        <strong>
                            {currency}
                            {grand_total:,.2f}
                        </strong>,

                        including

                        <strong>
                            {currency}
                            {additional_charge_total:,.2f}
                        </strong>

                        in additional charges.

                        <br><br>

                        These charges are separate from
                        the purchased items and taxes
                        and should be reviewed by the customer.

                    </div>
                    """
                )

            else:

                st.html(
                    """
                    <div class="verification-card">

                        <strong>
                            ✅ Bill total verified.
                        </strong>

                        <br><br>

                        The calculated bill total matches
                        the reported bill total, and no
                        additional non-item charges were detected.

                    </div>
                    """
                )

        elif total_difference > 0:

            st.html(
                f"""
                <div class="extra-card">

                    <h3>
                        ⚠️ Total Difference Detected
                    </h3>

                    <div class="extra-value">

                        {currency}
                        {total_difference:,.2f}

                    </div>

                    <p style="color:#9a3412;">

                        The reported bill total is higher
                        than the amount calculated from
                        the extracted items, taxes and
                        additional charges.

                    </p>

                </div>
                """
            )

        else:

            st.info(
                f"The calculated total is "
                f"{currency} "
                f"{abs(total_difference):,.2f} "
                "higher than the reported total."
            )

st.html(
    """
    <div class="footer">

        BillGuard · Understand your bill before you pay. ✨

    </div>
    """
)