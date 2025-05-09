import React, { useState, useEffect } from "react";
import { FaHome } from "react-icons/fa";
import "./nav.css";
import MenuBtn from "./Menubtn";
import UserIcon from "./UserIcon";
import { Link } from "react-router-dom";
import { LuScanLine } from "react-icons/lu";
import { get_gym_data } from "../../config/actions";

const Navbar = ({ menuState, setMenuState }) => {
    const [gymData, setGymData] = useState(null);
    const iconStyle = `text-[29px] text-white hover:text-accent cursor-pointer`;

    useEffect(() => {
        get_gym_data().then(({ gym_data }) => {
            setGymData(gym_data);
        });
    }, []);

    return (
        <nav
            className={`h-16 bg-primary flex items-center justify-between
                        px-8 lg:px-20 ${
                            menuState ? "ps-[250px] lg:ps-[300px]" : ""
                        } `}
        >
            {/* icons */}
            <div className="icons flex items-center">
                <MenuBtn menuState={menuState} setMenuState={setMenuState} />
                <Link to={"/"}>
                    <FaHome className={`${iconStyle} mx-4 lg:mx-7`} />
                </Link>
                <Link to={"/barcode/today"}>
                    <LuScanLine className={`${iconStyle}`} />
                </Link>
            </div>

            <h1 className="text-accent font-bold text-2xl hidden lg:block ">
                {gymData?.title}
            </h1>

            {/* user */}
            <UserIcon
                gymData={gymData}
                className={`${menuState && "hidden md:block"}`}
            />
        </nav>
    );
};

export default Navbar;
