function makeURL(route) {
    if (window.baseURL) return window.baseURL + route;
    return route;
}

export class Core {
    static makeRequest(route, body) {
        return new Promise((resolve, reject) => {
            fetch(makeURL(route), {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(body),
            }).then((r) => {
                r.json().then((data) => {
                    if (data.result != null && "error" in data.result) {
                        reject(data.result.error);
                        return;
                    }
                    resolve(data.result);
                });
            }).catch((e) => {
                reject(e);
            })
        });
    }
}

export class API {
    static login (str_user_i_d,str_password,str_url,str_connection,str_session_id,str_pin,) {

    return Core.makeRequest("/api/login/login", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        str_session_id: str_session_id,
        str_pin: str_pin,
        });
}

static sell_order (str_instr,amount,rate,order_type,str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/sell_order", {
        str_instr: str_instr,
        amount: amount,
        rate: rate,
        order_type: order_type,
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static buy_order (str_instr,amount,rate,order_type,str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/buy_order", {
        str_instr: str_instr,
        amount: amount,
        rate: rate,
        order_type: order_type,
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_orders_table_api (str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_orders_table_api", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_offers_table_api (str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_offers_table_api", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_accounts_table_api (str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_accounts_table_api", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_closed_trades_table_api (str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_closed_trades_table_api", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_messages_trades_table_api (str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_messages_trades_table_api", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_summary_trades_table_api (str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_summary_trades_table_api", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_trades_table_api (str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_trades_table_api", {
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}

static get_price_history (str_instr,str_user_i_d,str_password,str_url,str_connection,) {

    return Core.makeRequest("/api/tables/get_price_history", {
        str_instr: str_instr,
        str_user_i_d: str_user_i_d,
        str_password: str_password,
        str_url: str_url,
        str_connection: str_connection,
        });
}
}