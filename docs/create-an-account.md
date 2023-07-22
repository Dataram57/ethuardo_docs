# Create an Account
To create an account, you need to have access to your crypto wallet. And specifically to one of these listed blockchain networks:
- **Ethereum**
- **Polygon** (Recommended due to lower transaction fees)
Technically speaking, you will send a transaction on one of these blockchains, with an encrypted message containing a hash from your new password, that will be used for logging in. So go to [/register](https://ethuardo.com/register/), and:
1. Connect your wallet to the website, either with MetaMask or through the more universal WalletConnect protocol. If the wallet connects well, a border of the selected connection method will turn green.<br>
![Connect your wallet](/img/tutorial-register-wallet.png)
<br> *In the case of using a WalletConnect protocol, you will have to select the right network from your wallet side, which you won't be able to change later, without reconnecting the wallet.*
2. Enter additional deposit sum. (Optional)
3. Enter your new password for your new account. This new password **should not be your wallet's private key, keywords, or related to that**. This is your brand new password for the account on the Ethuardo and currently only on that platform.
4. Repeat your new password.
5. Click register.

Once you have clicked the register button, the procedure of making a transaction will happen:

![Transaction summary](/img/tutorial-register-tx.png)

By default, each transaction is currently sending a default minimum amount of money equal to 0.000001 of the currency that you have chosen.

![Transaction detail](/img/tutorial-register-tx-detail.png)

The message in the transaction contains a hash from the hash of your password salted with a login_index(used for logging in)

Once you have accepted the transaction, our servers will listen the blockchain to see if your transaction has found itself in a block, and then realise the action from the transaction message.

To check if the transaction was fully realised, click on the Orders icon to see the status of it.

![Registration complete](/img/tutorial-register-done.png)

If the transaction was successful, go to /login and try to login!