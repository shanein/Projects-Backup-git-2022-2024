defmodule CryptoApi.AccountsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `CryptoApi.Accounts` context.
  """

  @doc """
  Generate a user.
  """
  def user_fixture(attrs \\ %{}) do
    {:ok, user} =
      attrs
      |> Enum.into(%{
        email: "some email",
        firstname: "some firstname",
        lastname: "some lastname",
        password: "some password",
        role: "some role"
      })
      |> CryptoApi.Accounts.create_user()

    user
  end

  @doc """
  Generate a user_crypto.
  """
  def user_crypto_fixture(attrs \\ %{}) do
    {:ok, user_crypto} =
      attrs
      |> Enum.into(%{

      })
      |> CryptoApi.Accounts.create_user_crypto()

    user_crypto
  end
end
