import React from 'react'
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

import { AuthConsumer, AuthProvider } from '../contexts/AuthContext.js'
import ProtectedRoute from '../shared/ProtectedRoute.js'

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <div>
          {/* <AuthButton/> */}
          <ul>
            <li><Link to="/public">Public Page</Link></li>
            <li><Link to="/protected">Protected Page</Link></li>
          </ul>
          <Route path="/public" component={Public}/>
          <AuthConsumer>
            {user => <Route path="/login" user={user} component={Login}/> }
          </AuthConsumer>
          <ProtectedRoute path='/protected' component={Protected} />
        </div>
      </Router>
    </AuthProvider>
  )
}

const Public = () => {
  return (
    <AuthConsumer>
      {({ teacher_name }) => (
        <h1>{teacher_name}</h1>
      )}
    </AuthConsumer>
  )
}
const Protected = () => <h3>Protected</h3>

class Login extends React.Component {
  state = {
    redirectToReferrer: false
  }
  login = () => {
    console.log(this.props.user)
    // this.props.user.updateUser('foo@bar.com', 'Mr. Foo', '1234')
    this.setState(() => ({
      redirectToReferrer: true
    }))
  }
  render() {
    console.log(this.props.user)
    const { from } = this.props.location.state || { from: { pathname: '/' } }
    const { redirectToReferrer } = this.state

    if (redirectToReferrer === true) {
      return <Redirect to={from} />
    }

    return (
      <div>
        <p>You must log in to view the page</p>
        <button onClick={this.login}>Log in</button>
      </div>
    )
  }
}

function PrivateRoute ({ component: Component, ...args }) {
  return (
    <AuthConsumer>
      { user => {
        if (user.isAuthenticated) {
          return < Route {...args} render={(props) => <Component {...props} /> } />
        } else {
          return < Route {...args} render={(props) => <Redirect to={{ pathname: '/login', state: { from: props.location } }} /> } />
        }
       }
      }
    </AuthConsumer>
  )
}

// const AuthButton = withRouter(({ history }) => (
//   fakeAuth.isAuthenticated ? (
//     <p>
//       Welcome! <button onClick={() => {
//         fakeAuth.signout(() => history.push('/'))
//       }}>Sign out</button>
//     </p>
//   ) : (
//     <p>You are not logged in.</p>
//   )
// ))
