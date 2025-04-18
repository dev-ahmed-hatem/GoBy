import React, { useState, useEffect, useRef } from "react";
import { Table, Button } from "flowbite-react";
import Loading from "../groups/Loading";
import ViewGroup from "../groups/ViewGroup";
import TableGroup from "../groups/TableGroup";
import TablePagination from "../groups/TablePagination";
import endpoints from "../../config/config";
import SubscriptionCard from "../subscriptions/SubscriptionCard";
import { fetch_list_data } from "../../config/actions";
import ErrorGroup from "../groups/ErrorGroup";
import { usePermission } from "../../providers/PermissionProvider";
import JsBarcode from "jsbarcode";
import QRCode from "qrcode";

const ClientSearch = () => {
    //////////////////////////////// providers ////////////////////////////////
    const { set_page_permissions } = usePermission();

    //////////////////////////////// permissions ////////////////////////////////
    const permissions = set_page_permissions("clients", "client");
    const subscription_permissions = set_page_permissions(
        "subscriptions",
        "subscription"
    );
    if (!permissions.change && !permissions.view) {
        return (
            <p className="text-lg text-center text-red-600 py-4">
                ليس لديك صلاحيات هنا
            </p>
        );
    }

    //////////////////////////////// list data ////////////////////////////////
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [fetchError, setFetchError] = useState(null);
    const [searchParam, setSearchParam] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);
    const [currentClient, setCurrentClient] = useState(null);

    //////////////////////////////// ID data ////////////////////////////////
    const barcodeRef = useRef(null);
    const qrCodeRef = useRef(null);

    const get_current_clients = () => {
        const searchURL = `${endpoints.client_list}${
            searchParam ? `&client=${searchParam}` : ""
        }${pageNumber ? `&page=${pageNumber}` : ""}
        `;

        fetch_list_data({
            searchURL: searchURL,
            setData: setData,
            setFetchError: setFetchError,
            setLoading: setLoading,
        });
    };

    const get_client_data = (url) => {
        setLoading(true);
        fetch_list_data({
            searchURL: url,
            setData: setCurrentClient,
            setFetchError: setFetchError,
            setLoading: setLoading,
        });
    };

    const generate_qr_bar_codes = () => {
        if (currentClient?.id) {
            try {
                if (barcodeRef.current) {
                    // Generate Barcode
                    JsBarcode(barcodeRef.current, currentClient.id, {
                        format: "CODE128",
                        height: 130,
                        displayValue: true,
                    });
                }
            } catch (error) {
                console.error("Error generating barcode:", error);
                if (barcodeRef.current) {
                    barcodeRef.current.alt = "Failed to generate barcode.";
                }
            }

            try {
                if (qrCodeRef.current) {
                    // Generate QR Code
                    QRCode.toCanvas(qrCodeRef.current, String(currentClient.id), {
                        width: 130,
                        margin: 2,
                        errorCorrectionLevel: "H",
                    });
                }
            } catch (error) {
                console.error("Error generating QR code:", error);
                if (qrCodeRef.current) {
                    qrCodeRef.current.alt = "Failed to generate barcode.";
                }
            }
        }
    };

    useEffect(() => {
        if (permissions.view) {
            get_current_clients();
        }
    }, [searchParam, pageNumber]);

    useEffect(() => {
        generate_qr_bar_codes();
        const clientData = document.getElementById("client-data");
        if (clientData) {
            clientData.scrollIntoView({ behavior: "smooth" });
        }
    }, [currentClient]);

    if (!permissions.view)
        return (
            <ErrorGroup
                title={"العملاء الحاليين"}
                message={"ليس لديك صلاحية"}
            />
        );

    return (
        <>
            {/* table data */}
            <ViewGroup title={"العملاء الحاليين"}>
                {loading ? (
                    <Loading />
                ) : fetchError ? (
                    <p className="text-lg text-center text-red-600 py-4">
                        خطأ في تحميل البيانات
                    </p>
                ) : (
                    <>
                        <TableGroup
                            onChange={(event) => {
                                setPageNumber(null);
                                setSearchParam(event.target.value);
                            }}
                        >
                            {data.count == 0 ? (
                                <Table.Body>
                                    <Table.Row className="text-lg text-center text-gray-800 py-3 font-bold bg-red-500">
                                        <Table.Cell>لا توجد بيانات</Table.Cell>
                                    </Table.Row>
                                </Table.Body>
                            ) : (
                                <>
                                    <Table.Head>
                                        <Table.HeadCell>
                                            اسم العميل
                                        </Table.HeadCell>
                                        <Table.HeadCell className="text-center">
                                            كود العميل
                                        </Table.HeadCell>
                                        <Table.HeadCell></Table.HeadCell>
                                    </Table.Head>
                                    <Table.Body>
                                        {data.results.map((client) => {
                                            return (
                                                <Table.Row
                                                    key={client.id}
                                                    className="bg-white font-medium text-gray-900"
                                                >
                                                    <Table.Cell>
                                                        {client.name ? (
                                                            client.name
                                                        ) : (
                                                            <span className="text-red-600">
                                                                غير مسجل
                                                            </span>
                                                        )}
                                                    </Table.Cell>
                                                    <Table.Cell className="text-center">
                                                        {client.id ? (
                                                            client.id
                                                        ) : (
                                                            <span className="text-red-600">
                                                                غير مسجل
                                                            </span>
                                                        )}
                                                    </Table.Cell>
                                                    <Table.Cell>
                                                        <Button
                                                            color={"primary"}
                                                            className="w-28 h-10 flex justify-center items-center"
                                                            onClick={() => {
                                                                setCurrentClient(
                                                                    client
                                                                );
                                                            }}
                                                        >
                                                            <span>
                                                                عرض البيانات
                                                            </span>
                                                        </Button>
                                                    </Table.Cell>
                                                </Table.Row>
                                            );
                                        })}
                                    </Table.Body>
                                </>
                            )}
                        </TableGroup>

                        {data.total_pages > 1 && (
                            <TablePagination
                                totalPages={data.total_pages}
                                currentPage={data.current_page}
                                onPageChange={(page) => {
                                    setPageNumber(page);
                                }}
                            />
                        )}
                        <div className="flex justify-center text-lg">
                            العدد : {data.count} عميل
                        </div>
                    </>
                )}
            </ViewGroup>

            {/* client data */}
            {currentClient && (
                <div
                    id="client-data"
                    className={`client-data p-4 my-8 bg-white rounded border-t-4 border-primary shadow-lg`}
                >
                    <h1 className="font-bold text-text text-lg">بيانات عميل</h1>
                    <hr className="h-px my-3 bg-gray-200 border-0"></hr>
                    <div className="table-wrapper overflow-x-auto">
                        <Table className="text-right text-lg">
                            <Table.Body>
                                {/* photo */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">الصورة : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.photo ? (
                                                <img
                                                    src={currentClient.photo}
                                                    className="w-72"
                                                />
                                            ) : (
                                                <span className="text-secondary">
                                                    لا توجد صورة حالية
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* barocde */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            الباركود :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            <img
                                                ref={barcodeRef}
                                                // src={currentClient.barcode}
                                                // className="w-72"
                                            />
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* qrocde */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">ال qr : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            <canvas
                                                ref={qrCodeRef}
                                                // src={currentClient.qr_code}
                                                className="w-64"
                                            />
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* name */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">الاسم : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.name ? (
                                                <span>
                                                    {currentClient.name}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* id */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">الكود : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.id ? (
                                                <span>{currentClient.id}</span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* is blocked */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">محظور : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        {currentClient.is_blocked ? (
                                            <span className="text-secondary font-bold">
                                                نعم
                                            </span>
                                        ) : (
                                            <span>لا</span>
                                        )}
                                    </Table.Cell>
                                </Table.Row>
                                {/* phone */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            رقم الموبايل :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.phone ? (
                                                <span>
                                                    {currentClient.phone}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* phone2 */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            رقم الموبايل 2 :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.phone2 ? (
                                                <span>
                                                    {currentClient.phone2}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* national_id */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            رقم الهوية :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.national_id ? (
                                                <span>
                                                    {currentClient.national_id}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* gander */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">النوع : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.gander ? (
                                                <span>
                                                    {currentClient.gander ==
                                                    "male"
                                                        ? "ذكر"
                                                        : "أنثى"}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* birth date */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            تاريخ الميلاد :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.birth_date ? (
                                                <span>
                                                    {currentClient.birth_date}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* age */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">العمر : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.age ? (
                                                <span>{currentClient.age}</span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* email */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            البريد الالكترونى :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.email ? (
                                                <span>
                                                    {currentClient.email}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* address */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">العنوان : </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.address ? (
                                                <span>
                                                    {currentClient.address}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* trainer */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            تمت الإضافة فى :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.date_created ? (
                                                currentClient.date_created
                                            ) : (
                                                <span className="text-red-600">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                                {/* added by */}
                                <Table.Row>
                                    <Table.Cell>
                                        <span className="me-3">
                                            تمت الإضافة بواسطة :{" "}
                                        </span>
                                    </Table.Cell>
                                    <Table.Cell>
                                        <span>
                                            {currentClient?.added_by ? (
                                                <span>
                                                    {currentClient.added_by
                                                        ?.name ??
                                                        currentClient.added_by
                                                            ?.username}
                                                </span>
                                            ) : (
                                                <span className="text-secondary">
                                                    غير مسجل
                                                </span>
                                            )}
                                        </span>
                                    </Table.Cell>
                                </Table.Row>
                            </Table.Body>
                        </Table>
                    </div>
                </div>
            )}

            {/* client subscriptions */}
            {currentClient && (
                <div
                    className={`client-data p-4 my-8 bg-white rounded border-t-4 border-primary shadow-lg`}
                >
                    <h1 className="font-bold text-text text-lg">
                        سجل الاشتراكات
                    </h1>
                    <hr className="h-px my-3 bg-gray-200 border-0"></hr>
                    {subscription_permissions.view ? (
                        <>
                            {currentClient.subscriptions.length !== 0 ? (
                                <div className="subscriptions-wrapper flex gap-6 flex-wrap">
                                    {currentClient.subscriptions.map((sub) => (
                                        <SubscriptionCard
                                            key={sub?.id}
                                            sub={sub}
                                            callBack={() => {
                                                get_client_data(
                                                    currentClient.url
                                                );
                                            }}
                                            deleteCallBack={() => {
                                                get_client_data(
                                                    currentClient.url
                                                );
                                            }}
                                        />
                                    ))}
                                </div>
                            ) : (
                                <p>هذا العميل ليس لديه اشتراكات بعد </p>
                            )}
                        </>
                    ) : (
                        <p className="text-lg text-center text-red-600 py-4">
                            ليس لديك صلاحية
                        </p>
                    )}
                </div>
            )}
        </>
    );
};

export default ClientSearch;
