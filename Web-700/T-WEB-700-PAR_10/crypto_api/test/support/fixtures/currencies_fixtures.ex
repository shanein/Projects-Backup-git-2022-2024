defmodule CryptoApi.CurrenciesFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `CryptoApi.Currencies` context.
  """

  @doc """
  Generate a crypto.
  """
  def crypto_fixture(attrs \\ %{}) do
    {:ok, crypto} =
      attrs
      |> Enum.into(%{
        name: "some name"
      })
      |> CryptoApi.Currencies.create_crypto()

    crypto
  end
end
