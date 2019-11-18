import {AppBar, Button, IconButton, Link, ListItemText, makeStyles, Menu, MenuItem, Toolbar, Typography} from "@material-ui/core";
import AccountCircle from "@material-ui/icons/AccountCircle";
import MenuIcon from "@material-ui/icons/Menu";
import React from "react";
import {AuthConsumer} from "../contexts/AuthContext";

function LoginLogoutButton(props: any) {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleMenuOpen = (event: any) => {
        setAnchorEl(event.currentTarget);
    };
    const handleMenuClose = () => {
        setAnchorEl(null);
    };
    if (props.user.isAuthenticated) {
        return (
            <div>
                <IconButton
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    onClick={handleMenuOpen}
                    color="inherit"
                >
                    <AccountCircle  />
                </IconButton>
                <Menu
                    id="menu-appbar"
                    anchorEl={anchorEl}
                    anchorOrigin={{horizontal: "right", vertical: "top"}}
                    keepMounted={true}
                    transformOrigin={{horizontal: "right", vertical: "top"}}
                    open={open}
                    onClose={handleMenuClose}
                >
                    <Link color="inherit" href="/user/profile">
                        <MenuItem>
                                <ListItemText primary="Profile" />
                        </MenuItem>
                    </Link>
                    <Link color="inherit" href="/user/settings">
                        <MenuItem>
                                <ListItemText primary="Settings" />
                        </MenuItem>
                    </Link>
                    <Link color="inherit" href="/api/users/logout">
                        <MenuItem>
                                <ListItemText primary="Logout" />
                        </MenuItem>
                    </Link>
                </Menu>
            </div>
        );
    } else {
        return (
            <Button color="inherit" href="/api/users/oauth/cognito/login">Login</Button>
        );
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

const BCNavBar: React.FC = () => {
    const classes = useStyles();
    return (
        <AppBar position="static">
            <Toolbar>
            <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                <MenuIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
                bubblecheck.app
            </Typography>
            <AuthConsumer>
                {(authctx) => <LoginLogoutButton user={authctx.user} />}
            </AuthConsumer>
            </Toolbar>
        </AppBar>
    );
};

export default BCNavBar;
