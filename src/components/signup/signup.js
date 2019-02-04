import React from 'react';
import WOW from 'wowjs';
import {
    Card,
    Form,
    Button,
    Modal,
    Message
} from 'semantic-ui-react';
import './signup.css';
import {connect} from 'react-redux';
import {signup} from '../../services/store/actions/userActions';

class SignUp extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            firstname:"",
            lastname:"",
            email:"",
            password:"",
            username:"",
            cpassword:"",
            error:false
        }
    }

    componentDidMount(){
        var wow = new WOW.WOW();
        wow.init();
    }

    handleOnChange = (e) =>{
        var target = e.target;
        var name = target.name;
        var value = target.value;
        this.setState({
            [name]:value
        })
    }

    handleSignUp = () =>{
        var data = {
            firstname:this.state.firstname,
            lastname:this.state.lastname,
            email:this.state.email,
            password:this.state.password,
            username:this.state.username,
        }
        this.props.signup(data);
    }

    render(){
        const {error={}} = this.state;
        return(
            <Modal className="wow zoomIn" trigger={<Button content="Join our community"></Button>}>
                <Modal.Content>
            <Card className="signup wow bounceIn" data-wow-duration="400ms">
                <Card.Content className='header'>
                    Join our community
                </Card.Content>
                <Card.Content>
                <Form autofill="false">
                <Form.Input onChange={this.handleOnChange} icon='user' type="text" name="firstname" iconPosition='left' placeholder='First name' />
                <Form.Input onChange={this.handleOnChange} icon='user' type="text" name="lastname" iconPosition='left' placeholder='Last name' />
                <Form.Input required onChange={this.handleOnChange} icon='mail' type="email" name="email" iconPosition='left' placeholder='Email' />
                <Form.Input autofill="false" onChange={this.handleOnChange} icon="user" type="text" name="username" iconPosition="left" placeholder="Choose a username"/>
                <Form.Input autofill="false" onChange={this.handleOnChange} icon='lock' type="password" name="password" iconPosition='left' placeholder='Password' />
                <Form.Input onChange={this.handleOnChange} icon='lock' type="password" name="cpassword" iconPosition='left' placeholder='Confirm password' />
                <Button type="submit" onClick ={this.handleSignUp} content="Create account"/>
                </Form>
                {error ? <Card.Content className="wow slideInDown" data-wow-duration="400ms">
                    <Message className="wow fadeIn" warning>{error.responseJSON.error}</Message>
                </Card.Content>:null}
                </Card.Content>
            </Card>
            </Modal.Content>
            </Modal>
        );
    }
}

const mapStateToProps = state =>{
    return{
        authres:state.user.authres,
        error:state.user.error
    }
}

export default connect(mapStateToProps,{signup})(SignUp);