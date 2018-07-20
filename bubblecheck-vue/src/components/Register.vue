<template>
    <div>
        <form method="POST" action="/user/login">
            <fieldset>
                <legend class="doc">Register</legend>
                <div class="row responsive-label">
                    <div class="col-sm-12 col-md-3">
                        <label for="email">Email</label>
                    </div>
                    <div class="col-sm-12 col-md-7">
                        <input type="email" id="email" placeholder="Email Address" name="email" />
                    </div>
                </div>
                <div class="row responsive-label">
                    <div class="col-sm-12 col-md-3">
                        <label for="teachername">Teacher Name</label>
                    </div>
                    <div class="col-sm-12 col-md-7">
                        <input type="text" id="teachername" placeholder="e.g. Mrs. Smith" name="teachername" />
                    </div>
                </div>
                <div class="row responsive-label">
                    <div class="col-sm-12 col-md-3">
                        <label for="password">Password</label>
                    </div>
                    <div class="col-sm-12 col-md-7">
                        <input type="password" id="password" placeholder="Password" name="password"/>
                    </div>
                </div>
                <div class="row responsive-label">
                    <div class="col-sm-12 col-md-3">
                        <label for="repeatpassword">Repeat Password</label>
                    </div>
                    <div class="col-sm-12 col-md-7">
                        <input type="password" id="repeatpassword" placeholder="Password again" name="repeatpassword"/>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 col-md-7 col-md-offset-3">
                        <button type="submit">Sign In</button>
                    </div>
                </div>
            </fieldset>
        </form>
    </div>
</template>

<style>
.responsive-label {
    align-items:center
}
.responsive-label div input {
    width: 100%;
}
@media (min-width: 768px) {
    .responsive-label .col-md-3{text-align:right}
}
</style>
