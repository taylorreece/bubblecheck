// This Context will hold information about the currently logged in user, and will be consumed by components throught the application

import React from 'react'

const AuthContext = React.createContext({
    user: {
        isAuthenticated: false,
        teacher_name: '',
        email: '',
        usersid: '',
    },
    updateUser: (user) => {}
})

class AuthProvider extends React.Component {
    state = {
        user: {
            isAuthenticated: false,
            teacher_name: 'a',
            email: '',
            usersid: 'b',
        },
        updateUser: this.updateUser,
    }
    updateUser = (user) => {
        this.setState({
            user: {
                isAuthenticated: true,
                teacher_name: user.teacher_name,
                email: user.email,
                usersid: user.usersid,
            }
        })
    }

    render() {
        return (
            <AuthContext.Provider 
                value={{
                    user: this.state.user,
                    updateUser: this.updateUser
                }}
            >
                {this.props.children}
            </AuthContext.Provider>
        )
    }
}

const AuthConsumer = AuthContext.Consumer

export { AuthProvider, AuthConsumer }