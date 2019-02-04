import React from 'react';
import './landing.css';
import {Grid,Divider,Card} from 'semantic-ui-react';
import {connect} from 'react-redux';
import Login from '../../components/login/login';
import SignUp from '../../components/signup/signup';
import {Redirect} from 'react-router-dom';
import WOW from 'wowjs';
import $ from 'jquery';

class LandingPage extends React.Component{

    componentDidMount(){
        var wow = new WOW.WOW();
        wow.init();
    }

    showSignUp=()=>{
        $('.signupcontainer').removeClass('hide');
    }

    closeSignUp =() =>{
        $('.signupcontainer').addClass('hide');
    }

    render(){
        const {authres={}} = this.props;
        if(authres.loggedIn === true){
            return <Redirect to="/unicornattractor/dashboard"/>
        }
        return(
            <div className="landing" onClick={e => this.closeSignUp}>
            <Grid celled className="introcard" stackable>
                <Grid.Row className="row">
                    {/* User actions */}
                    <Grid.Column width={16} className="usersection">
                    <Card className="wow fadeIn" data-wow-duration="500ms">
                        <Card.Header>
                            Unicorn Attractor
                        </Card.Header>
                    <Login id="login"/>
                    </Card>
                    <Divider></Divider>
                    <SignUp/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return{
        authres:state.user.authres
    }
}

export default connect(mapStateToProps)(LandingPage);