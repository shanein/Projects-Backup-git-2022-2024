from database.database import Session, get_db, Base, engine
from controllers.authController import get_current_user_from_token, authenticate_admin
from sqladmin import Admin, ModelView, BaseView, expose
from sqladmin.authentication import AuthenticationBackend
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from models.User import User
from models.Campaign_Terminal import Campaign
from models.Cible import Cible
from models.videoModel import Video
from models.Campaign_Terminal import Terminal

app = FastAPI(
    title="Smart Display API",
    description="API for the Smart Display project Backend",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    swagger_css_url="/static/custom_swagger.css",
)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user = authenticate_admin(username, password, db=Session())
        if not user:
            return False
        request.session.update({"token": user.email})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        else:
            return True


authentication_backend = AdminAuth(secret_key="Test123")
admin = Admin(app, engine=engine, authentication_backend=authentication_backend)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.firstname,
        User.lastname,
        User.email,
        User.user_type,
        User.is_active,
        User.is_superuser,
    ]


class VideoAdmin(ModelView, model=Video):
    column_list = [
        Video.id,
        Video.path,
        Video.campaign_id,
    ]


class CampaignAdmin(ModelView, model=Campaign):
    column_list = [
        Campaign.id,
        Campaign.name,
        Campaign.description,
        Campaign.start_date,
        Campaign.end_date,
        Campaign.videos,
        Campaign.budget,
        Campaign.is_smart,
        Campaign.address,
        Campaign.postal_code,
        Campaign.is_active,
        Campaign.is_valid,
        Campaign.advertiser_id,
    ]


class CibleAdmin(ModelView, model=Cible):
    column_list = [
        Cible.id,
        Cible.age,
        Cible.genre,
        Cible.campaign_id,
    ]


class TerminalAdmin(ModelView, model=Terminal):
    column_list = [
        Terminal.id,
        Terminal.name,
        Terminal.place_type,
        Terminal.description,
        Terminal.localisation,
        Terminal.lat,
        Terminal.long,
        Terminal.start_date,
        Terminal.last_update,
        Terminal.unavailable_dates,
        Terminal.week_schedule,
        Terminal.is_active,
        Terminal.distributor_id,
    ]


admin.add_view(UserAdmin)
admin.add_view(CampaignAdmin)
admin.add_view(CibleAdmin)
admin.add_view(VideoAdmin)
admin.add_view(TerminalAdmin)
