import {Outlet} from "react-router"
import Navbar from "~/ui/Navbar";

export default function Entery(){
    return (
        <>
            <Navbar/>
            <div className="mx-auto max-w-7xl sm:px-6 lg:px-8">
                <Outlet/>
            </div>

        </>
    )
}