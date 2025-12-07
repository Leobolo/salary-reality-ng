import streamlit as st

# --- App Config ---
st.set_page_config(
    page_title="🇳🇬 Salary Reality Calculator",
    page_icon="💰",
    layout="centered"
)

# --- Title & Intro ---
st.title("🇳🇬 Salary Reality Calculator")
st.markdown(
    """
    See what your salary *really* leaves you with each month—after tax, transport, family support, and more.
    
    Built with ❤️ for young Nigerians tired of "₦3M salary" illusions.
    """
)

# --- Input Section ---
st.header("💼 Your Details")

col1, col2 = st.columns(2)

with col1:
    gross_annual = st.number_input(
        "Gross Annual Salary (₦)",
        min_value=0,
        value=0,
        step=100_000,
        help="Your total yearly salary before deductions"
    )

with col2:
    city = st.selectbox(
        "City",
        ["Lagos", "Ibadan", "Abeokuta", "Port Harcourt", "Other"],
        help="Used to estimate transport & housing costs"
    )

# Lifestyle & Obligations
st.subheader("🧍 Your Lifestyle")
walk_to_work = st.checkbox("✅ I walk to work (save transport cost)")

st.subheader("👨‍👩‍👧 Family & Home Support")
col3, col4 = st.columns(2)
with col3:
    family_support = st.number_input(
        "Monthly to family (e.g., mum/sister) (₦)",
        min_value=0,
        value=40_000,
        step=5_000
    )
with col4:
    house_upkeep = st.number_input(
        "House contribution (₦)",
        min_value=0,
        value=50_000,
        step=5_000,
        help="If you live with family or share rent"
    )

st.subheader("🎯 Future Goal (Optional)")
goal_amount = st.number_input(
    "Goal: Save for new phones (₦)",
    min_value=0,
    value=250_000,
    step=50_000,
    help="e.g., ₦150k for you + ₦100k for mum"
)

# --- Calculations ---
# --- Accurate Nigerian Tax Function ---
def calculate_nigeria_tax(gross_annual):
    if gross_annual <= 0:
        return {'paye_annual': 0.0, 'effective_tax_rate': 0.0}
    cra = max(200_000, 0.21 * gross_annual)
    taxable = max(0, gross_annual - cra)
    tax = 0
    remaining = taxable
    brackets = [
        (300_000, 0.07),
        (300_000, 0.11),
        (500_000, 0.15),
        (500_000, 0.19),
        (1_600_000, 0.21),
        (float('inf'), 0.24)
    ]
    for limit, rate in brackets:
        if remaining <= 0:
            break
        chargeable = min(remaining, limit)
        tax += chargeable * rate
        remaining -= limit
    effective_rate = (tax / gross_annual) * 100
    return {'paye_annual': tax, 'effective_tax_rate': effective_rate}

# --- Calculations ---
gross_monthly = gross_annual / 12 if gross_annual > 0 else 0

# Statutory deductions
pension = gross_monthly * 0.08
nhf = gross_monthly * 0.025

# Accurate PAYE tax
tax_details = calculate_nigeria_tax(gross_annual)
paye = tax_details['paye_annual'] / 12  # monthly

net_after_statutory = gross_monthly - (pension + nhf + paye)

# Variable Costs
if city == "Lagos":
    transport = 0 if walk_to_work else 15_000
    rent_share = 70_000
elif city in ["Ibadan", "Abeokuta"]:
    transport = 0 if walk_to_work else 8_000
    rent_share = 40_000
elif city == "Port Harcourt":
    transport = 0 if walk_to_work else 12_000
    rent_share = 55_000
else:  # Other
    transport = 0 if walk_to_work else 10_000
    rent_share = 50_000

# Total monthly outgoings
total_outgoings = transport + rent_share + family_support + house_upkeep
real_spendable = net_after_statutory - total_outgoings

# Savings projection
if real_spendable > 0:
    max_monthly_save = min(real_spendable * 0.3, real_spendable)
    months_to_goal = round(goal_amount / max_monthly_save) if max_monthly_save > 0 and goal_amount > 0 else float('inf')
else:
    max_monthly_save = 0
    months_to_goal = float('inf')