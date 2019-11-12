// This Context will hold information about the currently logged in user, and will be consumed by components throught the application

import React from 'react'
import ApiInterface from '../api/Api'

const AuthContext = React.createContext({
    user: {
        isAuthenticated: false,
        teacher_name: '',
        email: 'noemail',
        usersid: '',
    },
})

class AuthProvider extends React.Component {
    async getLoginInformation() {
        let api = new ApiInterface()
        let user = await api.getCurrentUser()
        this.setState({
            user: {
                isAuthenticated: user.isAuthenticated,
                teacher_name: user.teacher_name,
                email: user.email,
                usersid: user.id,
            }
        })
    }
    componentDidMount() {
        this.getLoginInformation()
    }
    state = {
        user: {
            isAuthenticated: false,
            teacher_name: '',
            email: '',
            usersid: '',
        },
    }
    render() {
        return (
            <AuthContext.Provider 
                value={{
                    user: this.state.user,
                }}
            >
                {this.props.children}
            </AuthContext.Provider>
        )
    }
}

const AuthConsumer = AuthContext.Consumer

export { AuthProvider, AuthConsumer }