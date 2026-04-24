def query_sql(user_input: str) -> dict:
    """
    Mock SQL tool for now.
    Later this will connect to SQLite / Delta Lake / Databricks.
    """

    mock_accounts = {
        "A001": {
            "department": "Treasury",
            "balance": 500000,
            "risk_score": 0.72
        },
        "A003": {
            "department": "Risk",
            "balance": 900000,
            "risk_score": 0.89
        }
    }

    # very simple account extraction
    account_id = None
    for key in mock_accounts:
        if key in user_input:
            account_id = key
            break

    if not account_id:
        return {
            "status": "error",
            "message": "No known account ID found."
        }

    return {
        "status": "success",
        "source": "sql_tool",
        "account_id": account_id,
        "data": mock_accounts[account_id]
    }