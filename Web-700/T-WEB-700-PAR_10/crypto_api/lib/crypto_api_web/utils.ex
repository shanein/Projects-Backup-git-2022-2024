defmodule CryptoApiWeb.Utils do
  use CryptoApiWeb, :view

  alias CryptoApiWeb.CryptoView

  def replaceCryptos(entries) do
    cryptos = Enum.map(entries, fn e -> e.crypto end)
    cryptos_from_data = CryptoView.getCryptoInfo(cryptos)
    Enum.map(entries, fn e ->
      if length(cryptos) > 1 do
        Map.put(e, :crypto, Enum.find(cryptos_from_data, fn c ->
          String.downcase(c["id"]) == e.crypto.name
        end))
      else
        Map.put(e, :crypto, cryptos_from_data)
      end
    end)
  end
end
