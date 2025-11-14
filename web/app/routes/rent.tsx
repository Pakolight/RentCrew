import React from 'react'
import Sidebar from "../ui/Sidebar.tsx";
import {Outlet} from "react-router"


export default function Rent() {
    return <>
        <Sidebar>
            <Outlet/>
        </Sidebar>

    </>
}