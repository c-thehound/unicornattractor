import React from 'react';
import './mainapp.css';
import {Switch,Route,Redirect} from 'react-router-dom';
import Dashboard from './dashboard/dashboard';
import CreateIssue from './createissue/createissue';
import Issues from './issues/issues';
import IssueView from './issues/issueView';
import MyIssues from './createdbyme/createdbyme';
import AssignedToMe from './assignedtome/assignedtome';

export default class AppMain extends React.Component{
    
    render(){
            return(
                <div className="main-app">
                <Switch>
                    <Route exact path="/unicornattractor/dashboard" component={Dashboard}/>
                    <Route exact path="/unicornattractor/createissue" component={CreateIssue}/>
                    <Route exact path="/unicornattractor/issues" component={Issues}/>
                    <Route path="/unicornattractor/issues/:issueid" component={IssueView}/>
                    <Route path='/unicornattractor/createdbyme' component={MyIssues}/>
                    <Route path="/unicornattractor/assignedtome" component={AssignedToMe}/>
                </Switch>
                </div>
            );
    }
}