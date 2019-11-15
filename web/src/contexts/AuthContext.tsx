// This Context will hold information about the currently logged in user,
// and will be consumed by components throught the application

import React from "react";
import ApiInterface from "../api/Api";

const AuthContext = React.createContext({
    user: {
        email: "noemail",
        isAuthenticated: false,
        teacher_name: "",
        usersid: "",
    },
});

class AuthProvider extends React.Component {
    public state = {
        user: {
            email: "",
            isAuthenticated: false,
            teacher_name: "",
            usersid: "",
        },
    };
    public async getLoginInformation() {
        const api = new ApiInterface();
        const user = await api.getCurrentUser();
        this.setState({
            user: {
                email: user.email,
                isAuthenticated: user.isAuthenticated,
                teacher_name: user.teacher_name,
                usersid: user.id,
            },
        });
    }
    public componentDidMount() {
        this.getLoginInformation();
    }
    public render() {
        return (
            <AuthContext.Provider
                value={{user: this.state.user}}
            >
                {this.props.children}
            </AuthContext.Provider>
        );
    }
}

const AuthConsumer = AuthContext.Consumer;

export { AuthProvider, AuthConsumer };
