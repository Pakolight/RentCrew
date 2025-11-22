import React from 'react'
import Sidebar from "../ui/Sidebar.tsx";
import {Outlet} from "react-router"
import Drawer from "~/ui/Drawer";


export default function Rent() {
    return <>
        <Sidebar>
            <Outlet/>
        </Sidebar>

    </>
}