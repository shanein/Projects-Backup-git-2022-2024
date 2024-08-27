defmodule CryptoApi.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start the Ecto repository
      CryptoApi.Repo,
      # Start the Telemetry supervisor
      CryptoApiWeb.Telemetry,
      # Start the PubSub system
      {Phoenix.PubSub, name: CryptoApi.PubSub},
      # Start the Endpoint (http/https)
      CryptoApiWeb.Endpoint,
      # Start a worker by calling: CryptoApi.Worker.start_link(arg)
      # {CryptoApi.Worker, arg}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: CryptoApi.Supervisor]

    sup = Supervisor.start_link(children, opts)
    InitDatabase.init_cryptos()
    InitDatabase.init_users()
    sup

  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    CryptoApiWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
