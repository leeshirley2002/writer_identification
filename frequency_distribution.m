function writer_distance = freq_dis(y,writer_index)
[row_a column_a]=size(y);
kmeans_data=y(:,2:column_a);
[IDX,C] = kmeans(kmeans_data,5)
all_writer=[];
for kk = 1:43
    writer_k=[];
    for i = 1:row_a
        if y(i,1)==kk
            writer_k=[writer_k; y(i,2:column_a)];
        end
    end
    [X,Y]=size(writer_k);
    writer1=writer_k(:,:);
    [M,N]=size(writer1);
    prob = [];
    for k = 1:M
        total=0;
        temp=[];
        for i = 1:5
            distant = 0;
            for j = 1:67
            distant=distant+(writer1(k,j)-C(i,j))^2;
            end
            total = total +1/distant;
            temp=[temp 1/distant];
        end
        prob= [prob;temp/total];
    end
    tf=sum(prob)/M;
    all_writer=[all_writer;tf];
end
 idf=log(sum(sum(all_writer))./sum(all_writer));
 
 
%%test%%
writer_k=[];
for i = 1:row_a
    if y(i,1)==writer_index
        writer_k=[writer_k; y(i,2:column_a)];
    end
end
[X,Y]=size(writer_k);
writer1=writer_k(1:X/8,:);
[M,N]=size(writer1);
prob = [];
for k = 1:M
    total=0;
    temp=[];
    for i = 1:5
        distant = 0;
        for j = 1:67
            distant=distant+(writer1(k,j)-C(i,j))^2;
        end
        total = total +1/distant;
        temp=[temp 1/distant];
    end
    prob= [prob;temp/total];
end
tf_test=sum(prob)/M;
w_dist=zeros(43,5);
for i = 1:43
    for j =1:5
        w_dist(i,j)=(all_writer(i,j)-tf_test(1,j))^2*idf(1,j)/(all_writer(i,j)+tf_test(1,j));
    end
end
writer_distance=sum(w_dist,2);
end
