    # Depositing small positive amount increases balance accordingly.
    account.deposit(1)
    assert account.balance == 1