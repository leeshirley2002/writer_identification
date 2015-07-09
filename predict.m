predict_result=[];
for j=38:43
    output=[];
    for i = 1:21
        filename=strcat(num2str(i),'.csv');
        data=csvread(filename);
        temp=freq_dis(data,j);
        output=[output temp];
        sum_output=sum(output,2);
        [predict_writer,column]=find(sum_output==min(sum_output));
    end
    predict_result=[predict_result;j predict_writer];
end
