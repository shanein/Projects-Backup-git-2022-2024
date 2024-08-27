defmodule Api.TimeFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Api.Time` context.
  """

  @doc """
  Generate a workingtime.
  """
  def workingtime_fixture(attrs \\ %{}) do
    {:ok, workingtime} =
      attrs
      |> Enum.into(%{
        end: ~N[2022-10-24 08:09:00],
        start: ~N[2022-10-24 08:09:00]
      })
      |> Api.Time.create_workingtime()

    workingtime
  end

  @doc """
  Generate a clock.
  """
  def clock_fixture(attrs \\ %{}) do
    {:ok, clock} =
      attrs
      |> Enum.into(%{
        status: true,
        time: ~N[2022-10-24 08:13:00]
      })
      |> Api.Time.create_clock()

    clock
  end
end
