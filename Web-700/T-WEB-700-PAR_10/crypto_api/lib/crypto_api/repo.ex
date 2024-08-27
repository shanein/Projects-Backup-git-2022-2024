defmodule CryptoApi.Repo do
  use Ecto.Repo,
    otp_app: :crypto_api,
    adapter: Ecto.Adapters.Postgres
end
