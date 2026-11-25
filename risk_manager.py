
# Vahid Trade AI
# Risk Management Engine

DEFAULT_RISK_PERCENT = 1.0
DEFAULT_MAX_RISK_PERCENT = 2.0
DEFAULT_STOP_PERCENT = 2.0


def calculate_position_size(
    capital,
    entry_price,
    stop_loss_price,
    risk_percent=DEFAULT_RISK_PERCENT
):
    """
    Calculate position size based on account risk.
    """

    if capital <= 0:
        raise ValueError("Capital must be greater than zero")

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero")

    if stop_loss_price <= 0:
        raise ValueError("Stop loss price must be greater than zero")

    if risk_percent <= 0 or risk_percent > 100:
        raise ValueError("Risk percent must be between 0 and 100")

    price_difference = abs(entry_price - stop_loss_price)

    if price_difference == 0:
        raise ValueError("Entry and stop loss cannot be equal")

    risk_amount = capital * (risk_percent / 100)

    position_size = risk_amount / price_difference

    return {
        "risk_amount": round(risk_amount, 2),
        "position_size": round(position_size, 8),
        "risk_percent": risk_percent
    }


def calculate_stop_loss(
    entry_price,
    direction,
    stop_percent=DEFAULT_STOP_PERCENT
):
    """
    Calculate stop loss price.
    """

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero")

    if stop_percent <= 0 or stop_percent >= 100:
        raise ValueError("Stop percent must be between 0 and 100")

    direction = direction.lower()

    if direction == "buy":
        stop_loss = entry_price * (1 - stop_percent / 100)

    elif direction == "sell":
        stop_loss = entry_price * (1 + stop_percent / 100)

    else:
        raise ValueError("Direction must be buy or sell")

    return round(stop_loss, 8)


def check_risk_limit(
    risk_percent,
    max_risk_percent=DEFAULT_MAX_RISK_PERCENT
):
    """
    Check whether trade risk is within the allowed limit.
    """

    if risk_percent < 0:
        return False

    return risk_percent <= max_risk_percent


def calculate_risk_reward(
    entry_price,
    stop_loss_price,
    take_profit_price
):
    """
    Calculate risk to reward ratio.
    """

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero")

    risk = abs(entry_price - stop_loss_price)
    reward = abs(take_profit_price - entry_price)

    if risk == 0:
        raise ValueError("Risk cannot be zero")

    return round(reward / risk, 2)
