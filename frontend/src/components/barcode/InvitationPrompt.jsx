import React, { useState } from "react";
import { Label, Button, TextInput } from "flowbite-react";
import { AiOutlineLoading } from "react-icons/ai";
import axios from "../../config/axiosconfig";
import endpoints from "../../config/config";
import { useToast } from "../../providers/ToastProvider";
import { HiUser } from "react-icons/hi";
import { useForm } from "react-hook-form";

const InvitationPrompt = ({ invitation, subscription, callBack }) => {
    const [post, setPost] = useState(false);
    const { showToast } = useToast();

    const {
        register,
        handleSubmit,
        formState: { errors },
        trigger,
    } = useForm();

    const submit = (data) => {
        setPost(true);
        data = {
            invitation: invitation.id,
            guest_name: data.name,
            subscription: subscription.id,
        };

        axios
            .post(endpoints.attendance, data)
            .then((response) => {
                showToast("تم تسجيل الحضور");
            })
            .catch((error) => {
                console.log(error);
                showToast("خطأ فى تنفيذ العملية", true);
            })
            .finally(() => {
                setPost(false);
                if (callBack) callBack();
            });
    };

    return (
        <div>
            <h1 className="text-text text-base lg:text-lg my-3">
                اسم العميل :{" "}
                <span className="text-primary font-bold ms-2 me-3 lg:me-5">
                    {subscription.client_name}
                </span>
                <br />
                كود العميل :{" "}
                <span className="text-primary font-bold ms-2">
                    {subscription.client_id}
                </span>
                <br />
                <br />
                الاشتراك :{" "}
                <span className="text-primary font-bold ms-2">
                    {subscription.plan.name}
                </span>
                <br />
                كود الاشتراك :{" "}
                <span className="text-primary font-bold ms-2">
                    {subscription.id}
                </span>
                <br />
            </h1>
            {subscription.is_blocked ? (
                <p className="text-base lg:text-2xl text-center text-red-600 py-4">
                    محظور
                </p>
            ) : !invitation.is_valid ? (
                <p className="text-base lg:text-lg text-center text-red-600 py-4">
                    كود دعوة منتهي
                </p>
            ) : (
                <>
                    <form onSubmit={handleSubmit(submit)}>
                        <div className="w-full lg:max-w-md lg:w-[30%]">
                            <div className="mb-2 block">
                                <Label htmlFor="name" value="اسم المدعو :" />
                            </div>
                            <TextInput
                                id="name"
                                type="text"
                                rightIcon={HiUser}
                                placeholder="اسم المدعو"
                                color={errors.name ? "failure" : "primary"}
                                {...register("name", {
                                    required: "هذا الحقل مطلوب",
                                })}
                                onBlur={() => trigger("name")}
                            />

                            {errors.name && (
                                <p className="error-message">
                                    {errors.name.message}
                                </p>
                            )}
                        </div>
                        <div className="flex flex-wrap max-h-12 min-w-full justify-center mt-3">
                            <Button
                                color={"primary"}
                                type="submit"
                                disabled={post}
                                className="h-14 flex justify-center items-center text-lg"
                                size={"xl"}
                                isProcessing={post}
                                processingSpinner={
                                    <AiOutlineLoading className="h-6 w-6 animate-spin" />
                                }
                            >
                                استخدام الدعوة
                            </Button>
                        </div>
                    </form>
                </>
            )}
        </div>
    );
};

export default InvitationPrompt;
