import {AppBar, Button, CssBaseline, IconButton, makeStyles, Toolbar, Typography} from "@material-ui/core";
import { Menu } from "@material-ui/icons";
import React from "react";
import {AuthConsumer, AuthProvider} from "./contexts/AuthContext";

function PrintUserInfo(props: any) {
  return (
    <div>
      User Id: {props.user.usersid} <br />
      Email: {props.user.email} <br />
      Teacher Name: {props.user.teacher_name} <br />
    </div>
  );
}

function LoginLogoutButton(props: any) {
  if (props.user.isAuthenticated) {
    return (<Button color="inherit" href="/api/users/logout">Logout</Button>);
  } else {
    return (<Button color="inherit" href="/api/users/oauth/cognito/login">Login</Button>);
  }
}

const useStyles = makeStyles((theme) => ({
  menuButton: {
    marginRight: theme.spacing(2),
  },
  root: {
    flexGrow: 1,
  },
  title: {
    flexGrow: 1,
  },
}));

const App: React.FC = () => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <AuthProvider>
        <div className={classes.root}>
          <CssBaseline />
          <AppBar position="static">
            <Toolbar>
              <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                <Menu />
              </IconButton>
              <Typography variant="h6" className={classes.title}>
                bubblecheck.app
              </Typography>
              <AuthConsumer>
                {(authctx) => <LoginLogoutButton user={authctx.user} />}
              </AuthConsumer>
            </Toolbar>
          </AppBar>
            <AuthConsumer>
              {(authctx) => <PrintUserInfo user={authctx.user} />}
            </AuthConsumer>
        </div>
      </AuthProvider>
    </React.Fragment>
  );
};

export default App;
