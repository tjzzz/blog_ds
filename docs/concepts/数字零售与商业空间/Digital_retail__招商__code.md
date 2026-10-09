---
title: "code"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/08_业务专题/Digital_retail/招商/code.md"]
wiki_type: concepts
topic: "数字零售与商业空间"
migrated_from: "08_业务专题/Digital_retail/招商/code.md"
review_status: structural
---

> 所属 Topic：[数字零售与商业空间](../../topics/%E6%95%B0%E5%AD%97%E9%9B%B6%E5%94%AE%E4%B8%8E%E5%95%86%E4%B8%9A%E7%A9%BA%E9%97%B4.md) · 类型：概念

The main function of GA (Since the complete program is quite long, only the main function is listed here. As you can see, the main function structure is consistent with table 2.):

```matlab
%遗传主函数 function main()

clear;  
clc;  
close all  
%除了 initpop 之外，都要输入完整的购物中心种群 for daxunhuan = 1:4

%%

%楼层信息

Fn = 6;%楼层总数

Ch = 7;%楼层的物理特征数(一楼不包括入口)

%f = 1;%楼层

%G = 10000;%f 层的可出租面积

%% %店铺信息

%s = [];%楼层店铺面积矩阵

%x = [];%楼层店铺中心点 x 坐标

%y = [];%楼层店铺中心点 y 坐标

%% %楼层设施信息

%elevx = [];%楼层 f 的电梯中心点 x 坐标 %elevy = [];%楼层 f 的电梯中心点 y 坐标

ShMph = charac_1(Fn, Ch); %ShMph:(楼层总面积)，(单个店铺面积)，(店铺中心点坐标)，(电梯中心点

坐标)

entrx = [700.9109 645.4463 641.2834 641.0279 650.5831 650.8711 727.4578 725.0332

];%1 楼入口 x 坐标 entry = [2542.0152 2534.1304 2526.4701 2519.3482 2496.0956 2484.8699 2490.7176 2504.4124

];%1 楼入口 y 坐标 %%

%市场信息

n_i = [10000 3000  
365  
100000

500  
16320  
40320  
40800  
176000  
20460  
95040  
79200  
41580  
107800  
648000  
192000  
79200  
34560  
43200  
38880  
138240  
7056  
];%购物中心零售类型 i 的潜在消费者人数，22*1 cost_i = [200

1500  
5000  
30  
3000  
50  
60  
80  
15  
25  
25  
80  
100  
20  
60  
100  
200  
400  
200  
300  
200  
600  
];%零售类型 i 的潜在消费者每年愿意在 i 商品上花费的金额，22*1 %%

%开发者偏好

f_t = [  
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,...%这里是第 12 个

0, 0, 0, 0, 0, 0, 0, 0, 1, 1;%1 楼:21、22; 3、5

%  
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,...  
0, 0, 0, 0, 1, 0, 0, 0, 0, 0;%2楼:17;3  
%  
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,...  
0, 0, 0, 0, 1, 1, 0, 0, 0, 0;%3 楼:17、18;3  
%  
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,...  
0, 1, 0, 0, 0, 1, 0, 1, 0, 0;%4 楼:14、18、20;4、3、3 %  
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,...  
1, 0, 0, 0, 0, 0, 0, 0, 0, 0;%5 楼:12、13;4、4

0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,...  
0, 1, 1, 1, 0, 0, 0, 0, 0, 0;%B1 楼:9、10、11、14、15、16;2、4、4、4、1、1 ];%楼层主题调整矩阵

% f_t = [

%  
%  
%  
%  
%  
%  
%  
%  
%  
%  
%  
%  
%  
rB =  
%cf = 0.5^f;%楼层的基本租金调节系数 %%

0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8,...  
0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1, 1;%1 楼:21、22 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8,...  
0.8, 0.8, 0.8, 0.8, 1, 0.8, 0.8, 0.8, 0.8, 0.8;%2 楼:17  
0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8,...  
0.8, 0.8, 0.8, 0.8, 1, 1, 0.8, 0.8, 0.8, 0.8;%3 楼:17、18 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8,...  
0.8, 1, 0.8, 0.8, 0.8, 1, 0.8, 1, 0.8, 0.8;%4 楼:14、18、20 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1,...

1, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8;%5 楼:12、13  
0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1, 1, 1, 0.8,...%第 12 个  
0.8, 1, 1, 1, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8;%B1 楼:9、10、11、14、15、16 ];%楼层主题调整矩阵(7.10 的无奈之举)  
20;%1 楼每平方米每月基本租金

%算法参数设定  
popsize = 5000;%种群大小  
%n = length(s);%单层店铺数  
%chromlength = 2*n;%基因长度  
pc = 0.8;%交叉概率  
pm = 0.003;%变异概率  
ShMve = charac_2(ShMph, Fn, popsize, f_t);%初始化整个购物中心的种群 iter = 400;%迭代次数

elite = [];%每一代的最优精英个体  
elite_fitvalue = [];%每一代的最大适应度 fitvalue_mean = [];%每一代的平均适应度  
%%  
%迭代开始  
%1 次运行，要获得多个最优解需要进行多次运行 for i = 1:iter

disp('现在迭代代数为:');i%代数计数  
%计算适应度  
[objvalue, fit_mean] = cal_objvalue(ShMve, ShMph, entrx, entry, Fn, rB,...

n_i, cost_i, f_t);  
fitvalue = objvalue;%objvalue 为整个购物中心的总租金

fitvalue_best = max(fitvalue);%第 iter 代最大适应度 fitvalue_mean(i) = fit_mean;%第 iter 代平均适应度

%%  
%寻找最优解和精英  
%在这一步我们对 ShMve 根据 fitvalue 的大小进行排序了 [bestindividual, bestfit, ShMve, fitvalue] = best(ShMve, fitvalue, Fn); elite{i, 1} = bestindividual;%记录第 iter 代精英  
elite_fitvalue(i) = bestfit;%记录第 iter 代最大适应度  
%%  
%选择操作

newShMve = selection(ShMve, ShMph, Fn, popsize, fitvalue, i, f_t); %%  
%交叉操作  
newShMve = crossover(newShMve, pc, Fn);

%%

%变异操作

newShMve = mutation(newShMve, Fn, pm, ShMph, f_t); %%  
%添加精英  
%精英不参与交叉、变异，直接替换掉第 popsize 个个体 for ftemp = 1:Fn

yetai = newShMve{ftemp, 1};  
dengji = newShMve{ftemp, 2}; yetai(popsize, :) = bestindividual{ftemp, 1}; dengji(popsize, :) = bestindividual{ftemp, 2}; newShMve{ftemp, 1} = yetai; newShMve{ftemp, 2} = dengji;

end  
%%  
%更新种群  
ShMve = newShMve;

end  
%% %画图操作

x_iter = 1:iter;  
%figure  
plot(x_iter, elite_fitvalue, 'linewidth', 2.5);  
hold on;  
plot(x_iter, fitvalue_mean);  
fprintf('The best Y is --->%5.2f\n', max(elite_fitvalue));  
for emmm = 1:6  
myelite = [[elite{1, 1}{emmm, 1}],[elite{1, 1}{emmm, 2}]] end  
eval(['save process', num2str(daxunhuan)]);  
fid = fopen('outcome', 'a+');  
fprintf(fid, '%s', '运行次数:');  
fprintf(fid, '%d\n\r', daxunhuan);  
fprintf(fid, '%s\n\r', '这是最大的租金 max(elite_fitvalue):'); fprintf(fid, '%f\n\r', max(elite_fitvalue));  
fprintf(fid, '%s\n\r', '这是 myelite:');  
fprintf(fid, '%d\n\r', [[elite{1, 1}{1, 1}],[elite{1, 1}{1, 2}]]); fprintf(fid, '%d\n\r', [[elite{1, 1}{2, 1}],[elite{1, 1}{2, 2}]]); fprintf(fid, '%d\n\r', [[elite{1, 1}{3, 1}],[elite{1, 1}{3, 2}]]); fprintf(fid, '%d\n\r', [[elite{1, 1}{4, 1}],[elite{1, 1}{4, 2}]]); fprintf(fid, '%d\n\r', [[elite{1, 1}{5, 1}],[elite{1, 1}{5, 2}]]); fprintf(fid, '%d\n\r', [[elite{1, 1}{6, 1}],[elite{1, 1}{6, 2}]]); fclose(fid);  
end
```


