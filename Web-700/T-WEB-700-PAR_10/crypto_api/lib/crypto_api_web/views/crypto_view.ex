defmodule CryptoApiWeb.CryptoView do
  use CryptoApiWeb, :view
  alias CryptoApiWeb.CryptoView

  def render("index.json", %{cryptos: cryptos}) do
    %{data: getCryptoInfo(cryptos)}
  end

  def render("show.json", %{crypto: crypto}) do
    %{data: getCryptoInfo([crypto])}
  end

  def render("show_detail.json", %{crypto: crypto}) do
    getCryptoDetail(crypto)
  end

  def render("show_variation.json", %{crypto: crypto, length: length}) do
    getCryptoVariations(crypto, length)
  end

  def render("crypto_data.json", %{crypto: crypto}) do
    getCryptoInfo([crypto])
  end

  def render("crypto.json", %{crypto: crypto}) do
    %{
      name: crypto.name
    }
  end

  def getCryptoInfo(cryptos) do
    list_cryptos = Enum.map(cryptos, fn x -> x.name end)
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" <> Enum.join(list_cryptos, "%2C") <> "&order=market_cap_desc&page=1&sparkline=false"
    case HTTPoison.get(url) do
      {:ok, %{status_code: 200, body: body}} ->
        if length(cryptos) > 1 do
          Poison.decode!(body)
        else
          List.first(Poison.decode!(body))
        end
      {:ok, %{status_code: 404}} ->
        IO.puts("Request not found")
        if length(cryptos) > 1 do
          render_many(cryptos, CryptoView, "crypto.json")
        else
          render_one(List.first(cryptos), CryptoView, "crypto.json")
        end
      {:error, %{reason: reason}} ->
        IO.inspect(reason)
        if length(cryptos) > 1 do
          render_many(cryptos, CryptoView, "crypto.json")
        else
          render_one(List.first(cryptos), CryptoView, "crypto.json")
        end
    end
  end

  def getCryptoVariations(crypto, length) do
    url = "https://api.coingecko.com/api/v3/coins/" <> crypto.name <> "/ohlc?vs_currency=usd&days=" <> length
    case HTTPoison.get(url) do
      {:ok, %{status_code: 200, body: body}} ->
        Poison.decode!(body)
      {:ok, %{status_code: 404}} ->
        IO.puts("Request not found")
        render_one(crypto, CryptoView, "crypto.json")
      {:error, %{reason: reason}} ->
        IO.inspect(reason)
        render_one(crypto, CryptoView, "crypto.json")
    end
  end

  def getCryptoDetail(crypto) do
    url = "https://api.coingecko.com/api/v3/coins/" <> crypto.name <> "?tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    case HTTPoison.get(url) do
      {:ok, %{status_code: 200, body: body}} ->
        Poison.decode!(body)
      {:ok, %{status_code: 404}} ->
        IO.puts("Request not found")
        render_one(crypto, CryptoView, "crypto.json")
      {:error, %{reason: reason}} ->
        IO.inspect(reason)
        render_one(crypto, CryptoView, "crypto.json")
    end
  end
end
