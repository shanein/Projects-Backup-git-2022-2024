defmodule ApiWeb.WorkingtimeController do
  use ApiWeb, :controller

  alias Api.Time
  alias Api.Time.Workingtime

  action_fallback ApiWeb.FallbackController

  def showAll(conn, attr) do
    workingtimes = Time.get_all_workingtimes!(attr["user"], attr["start"], attr["end"])
    if workingtimes == [] do
      raise Ecto.NoResultsError, message: "No entry found with given fields"
    end
    render(conn, "index.json", workingtimes: workingtimes)
  end

  def showOne(conn, %{"user" => userID, "id" => id}) do
    workingtime = Time.get_one_workingtime!(userID, id)
    render(conn, "show.json", workingtime: workingtime)
  end

  def create(conn, %{"user" => userID, "workingtime" => workingtime_params}) do

    #Check if user id given in body and in the url does match
    if workingtime_params["user_id"] != nil do
      if workingtime_params["user_id"] != userID do
        raise ArgumentError, message: "The 'user_id' given in request does not match 'user_id' in URL."
      end
    end

    #Force user_id from URL by default
    workingtime_params = Map.put(workingtime_params, "user_id", userID)

    with {:ok, %Workingtime{} = workingtime} <- Time.create_workingtime(workingtime_params) do
      conn
      |> put_status(:created)
      |> put_resp_header("location", Routes.workingtime_path(conn, :showAll, workingtime))
      |> render("show.json", workingtime: workingtime)
    end
  end

  def update(conn, %{"id" => id, "workingtime" => workingtime_params}) do
    workingtime = Time.get_workingtime!(id)
    with {:ok, %Workingtime{} = workingtime} <- Time.update_workingtime(workingtime, workingtime_params) do
      render(conn, "show.json", workingtime: workingtime)
    end
  end

  def delete(conn, %{"id" => id}) do
    workingtime = Time.get_workingtime!(id)
    with {:ok, %Workingtime{}} <- Time.delete_workingtime(workingtime) do
      send_resp(conn, :no_content, "")
    end
  end
end
