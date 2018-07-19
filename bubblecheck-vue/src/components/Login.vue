<template>
    <div>
        <form method="POST" action="/user/login">
            <fieldset>
                <legend class="doc">Log In</legend>
                <div class="row responsive-label">
                    <div class="col-sm-12 col-md-3">
                        <label for="email" class="">Email</label>
                    </div>
                    <div class="col-sm-12 col-md-9">
                        <input type="email" id="email" placeholder="email" name="email"/>
                    </div>
                </div>
                <div class="row responsive-label">
                    <div class="col-sm-12 col-md-3">
                        <label for="password">Password</label>
                    </div>
                    <div class="col-sm-12 col-md-9">
                        <input type="password" id="password" placeholder="Password" name="password"/>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 col-md-9 col-md-offset-3">
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
@media (min-width: 768px) {
    .responsive-label .col-md-3{text-align:right}
}
</style>
