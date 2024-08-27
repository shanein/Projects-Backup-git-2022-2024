defmodule CryptoApiWeb.UserCryptoView do
  use CryptoApiWeb, :view
  alias CryptoApiWeb.UserCryptoView

  alias CryptoApiWeb.Utils
  alias CryptoApiWeb.CryptoView

  def render("index.json", %{users_cryptos: users_cryptos}) do
    users_cryptos = Utils.replaceCryptos(users_cryptos)
    %{data: render_many(users_cryptos, UserCryptoView, "user_crypto.json")}
  end

  def render("show.json", %{user_crypto: user_crypto}) do
    user_crypto = Map.put(user_crypto, :crypto, CryptoView.getCryptoInfo([user_crypto.crypto]))
    %{data: render_one(user_crypto, UserCryptoView, "user_crypto.json")}
  end

  def render("show-basic.json", %{user_crypto: user_crypto}) do
    %{
      user_id: user_crypto.user_id,
      crypto: %{
        name: user_crypto.crypto.name,
        id: user_crypto.crypto.id
      }
    }
  end

  def render("user_crypto.json", %{user_crypto: user_crypto}) do
    %{
      user_id: user_crypto.user_id,
      crypto: user_crypto.crypto
    }
  end
end
