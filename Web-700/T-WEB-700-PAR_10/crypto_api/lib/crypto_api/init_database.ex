defmodule InitDatabase do
  def init_cryptos do
    #Check if db is empty
    db_cryptos = CryptoApi.Currencies.list_cryptos()
    if length(db_cryptos) == 0 do
      url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=&order=market_cap_desc&per_page=10&page=1&sparkline=false"      #Add 10 default cryptos if yes
      case HTTPoison.get(url) do
        {:ok, %{status_code: 200, body: body}} ->
          cryptos = Poison.decode!(body)
          for crypto <- cryptos do
            CryptoApi.Repo.insert!(%CryptoApi.Currencies.Crypto{
              name: crypto["id"]
            })
          end
        {:ok, %{status_code: 404}} ->
          IO.puts("Request not found")
        {:error, %{reason: reason}} ->
          IO.inspect(reason)
      end
    end
  end

  def init_users do
    db_users = CryptoApi.Accounts.list_users()
    admin_in_db = Enum.find(db_users, fn u -> u.role == "admin" end)
    if admin_in_db == nil do
      CryptoApi.Repo.insert!(%CryptoApi.Accounts.User{
        email: "admin@apis.com",
        password: Bcrypt.Base.hash_password("admin", Bcrypt.Base.gen_salt(12, true)),
        role: "admin"
      })
    end
  end
end
