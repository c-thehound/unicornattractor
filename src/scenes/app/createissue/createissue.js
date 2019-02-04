import React from 'react';
import {connect} from 'react-redux';
import {createIssue} from '../../../services/store/actions/issueActions';
import {Form,Modal, Button} from 'semantic-ui-react';
import ReactQuill from 'react-quill';
import './createissue.css';
import $ from 'jquery';
import 'react-quill/dist/quill.bubble.css';
import WOW from 'wowjs';

class CreateIssue extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            type:null,
            title:"",
            detail:"",
            attemptedsolution:""
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

    componentDidUpdate(){
        $('.types button').removeClass('active');
        $(`.types .${this.state.type}`).addClass("active");
    }

    handleTypeSelect = (choice) =>{
        this.setState({
            type:choice
        })
    }

    handleSubmit = () =>{
        var data = {
            reporter:this.props.authres.username,
            type:this.state.type.toUpperCase(),
            title:this.state.title,
            detail:this.state.detail,
            attemptedsolution:this.state.attemptedsolution
        }
        this.props.createIssue(data,this.props.authres.token)
    }

    handleDetailChange = (value) =>{
        this.setState({detail:value})
    }
    handleAttSolutionChange = (value) =>{
        this.setState({attemptedsolution:value})
    }

    render(){
        return(
            <Modal className="wow zoomIn fadeIn" data-wow-duration="400ms" trigger={<Button className="newissue btn">New issue</Button>}>
                <Modal.Header>
                    Create a new issue
                    <div className="types">
                    <Button className="bug" onClick={e => this.handleTypeSelect("bug")}>Bug</Button>
                    <Button className="feature" onClick={e => this.handleTypeSelect("feature")}>Feature request</Button>
                    <span>Tell us whether you are reporting a bug or requesting a feature</span>
                    </div>
                </Modal.Header>
                <Modal.Content>
                    <Form>
                        <Form.Input type="text" placeholder="Title" name="title" onChange={this.handleOnChange}/>
                        <ReactQuill 
                        theme="bubble"
                        onChange={this.handleDetailChange}
                        value={this.state.detail}
                        modules={CreateIssue.modules}
                        formats={CreateIssue.formats}
                        bounds={'.app'}
                        placeholder="Write down a detailed description of your issue."
                        /><br></br>
                        <ReactQuill 
                        theme="bubble"
                        onChange={this.handleAttSolutionChange}
                        value={this.state.attemptedsolution}
                        modules={CreateIssue.modules}
                        formats={CreateIssue.formats}
                        bounds={'.app'}
                        placeholder="Have you tried to solve these issue ? Tell us how. (Optional)"
                        />
                        <Form.Button className="primary" onClick={this.handleSubmit}>Continue</Form.Button>
                    </Form>
                </Modal.Content>
            </Modal>
        );
    }
}


/* 
 * Quill modules to attach to editor
 * See https://quilljs.com/docs/modules/ for complete options
 */
CreateIssue.modules = {
    toolbar: [
      [{ 'header': '1'}, {'header': '2'}, { 'font': [] }],
      [{size: []}],
      ['bold', 'italic', 'underline', 'strike', 'blockquote'],
      [{'list': 'ordered'}, {'list': 'bullet'}, 
       {'indent': '-1'}, {'indent': '+1'}],
      ['link', 'image', 'video'],
      ['clean']
    ],
    clipboard: {
      // toggle to add extra line breaks when pasting HTML:
      matchVisual: false,
    }
  }

/* 
 * Quill editor formats
 * See https://quilljs.com/docs/formats/
 */
CreateIssue.formats = [
    'header', 'font', 'size',
    'bold', 'italic', 'underline', 'strike', 'blockquote',
    'list', 'bullet', 'indent',
    'link', 'image', 'video'
  ]

const mapStateToProps = state =>{
    return{
        authres:state.user.authres,
        issue:state.issues.issue
    }
}

export default connect(mapStateToProps,{createIssue})(CreateIssue);