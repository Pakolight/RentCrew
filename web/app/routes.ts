
import {
  type RouteConfig,
  route,
  layout,
  index,
  prefix,
} from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("login", "routes/login.tsx"),
    layout("routes/entery.tsx", [
        route("registration", "routes/registration.tsx"),
    ]),
    layout( "routes/rent.tsx", [
        route("calendar", "routes/calendar.tsx"),
        route("catalog-items", "routes/catalog-items.tsx"),

    ]),

] satisfies RouteConfig;
