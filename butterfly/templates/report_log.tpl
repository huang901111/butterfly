<!DOCTYPE html>
<html>
    <head>
        <title>Butterfly 访问日志分析</title>
        <meta charset="utf-8" />
        <link href="https://cdn.bootcss.com/twitter-bootstrap/3.4.1/css/bootstrap.min.css" rel="stylesheet" type="text/css">
        <script src="https://cdn.bootcss.com/jquery/2.2.4/jquery.min.js"></script>
        <script src="https://cdn.bootcss.com/twitter-bootstrap/3.4.1/js/bootstrap.min.js"></script>
        <script src="https://cdn.bootcss.com/echarts/4.3.0/echarts.min.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="col-md-12 text-center">
                    <hr>
                    <h1>Butterfly 访问日志分析</h1>
                    <hr>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="tile">
                        <h3>1. 概览</h3>
                        <div class="row">
                            <div class="col-md-12">
                                <div class="widget-small primary"><i class="icon fa fa-chain fa-3x"></i>
                                    <div class="info">
                                        <p>总访问量:{{ total_data.hits }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <h3>2. 状态码分布图</h3>
                                <div id="status" style="width:100%; height:400px;"></div>
                            </div>
                            <div class="col-md-6">
                                <h3>3. 用户访问分布量</h3>
                                <div id="users" style="width:100%; height:400px;"></div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <h3>4. 认证请求路径分布图</h3>
                                <div id="authpath" style="width:100%; height:400px;"></div>
                            </div>
                            <div class="col-md-6">
                                <h3>5. 每天访问量</h3>
                                <div id="hits" style="width:100%; height:400px;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <script type="text/javascript">
            var status_option = {
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                toolbox: {
                    show : false
                },
                calculable : true,
                series : [
                    {
                        name:'状态码状态分布',
                        type:'pie',
                        radius : '55%',
                        center: ['50%', '50%'],
                        data:[]
                    }
                ]
            };
            var users_option = {
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                toolbox: {
                    show : false
                },
                calculable : true,
                series : [
                    {
                        name:'用户分布',
                        type:'pie',
                        radius : '55%',
                        center: ['50%', '50%'],
                        data:[]
                    }
                ]
            };
            var authpath_option = {
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                toolbox: {
                    show : false
                },
                calculable : true,
                series : [
                    {
                        name:'认证路径',
                        type:'pie',
                        radius : '55%',
                        center: ['50%', '50%'],
                        data:[]
                    }
                ]
            };
            var hits_option = {
                tooltip : {
                    trigger: 'axis'
                },
                toolbox: {
                    show : false
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : []
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'访问量',
                        type:'line',
                        stack: '访问量',
                        data:[]
                    }
                ]
            };
            jQuery(document).ready(function() {
                var day_data={{ day_data|tojson }},
                    total_data={{ total_data|tojson }};

                var status_data = [];
                jQuery.each(total_data["status"], function(name, value) {
                    status_data.push({value:value, name:name});
                });

                var users_data = [];
                jQuery.each(total_data["users"], function(name, value) {
                    users_data.push({value:value, name:name});
                });

                var authpath_data = [];
                jQuery.each(total_data["authpath"], function(name, value) {
                    authpath_data.push({value:value, name:name});
                });

                var day_xAxis = [];
                var hits_data = [];

                jQuery.each(day_data, function(index, value) {
                    day_xAxis.push(value[0]);
                    hits_data.push(value[1]['hits']);
                });

                var status_chart = echarts.init(document.getElementById('status'));
                status_option["series"][0]["data"] = status_data;
                status_chart.setOption(status_option);

                var users_chart = echarts.init(document.getElementById('users'));
                users_option["series"][0]["data"] = users_data;
                users_chart.setOption(users_option);

                var authpath_chart = echarts.init(document.getElementById('authpath'));
                authpath_option["series"][0]["data"] = authpath_data;
                authpath_chart.setOption(authpath_option);

                var hits_chart = echarts.init(document.getElementById('hits'));
                hits_option["xAxis"][0]["data"] = day_xAxis;
                hits_option["series"][0]["data"] = hits_data;
                hits_chart.setOption(hits_option);

            });
        </script>
    </body>
</html>


