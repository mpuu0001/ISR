rm(list =ls())
setwd('/Users/apple/Library/Preferences/PyCharmCE2019.1/scratches/iSR-master/code_payload/run_length/data')

# Read data 
# DS = read.csv("data_partial.csv")
DS = read.csv("data.csv")

# Calculate each compression ratio 
DS$comp_ratio = 1 - round((DS$new_payload / DS$original_payload),2)
comp = count(DS, DS$comp_ratio) 
colnames(comp) = c('comp_ratio','freq')

# Change ratio to factor
comp$ratio = ifelse(comp$comp_ratio < 0, '< 0', NA)
comp$ratio = ifelse(comp$comp_ratio < 0.3 & comp$comp_ratio >= 0, '< 0.3', comp$ratio)
comp$ratio = ifelse(comp$comp_ratio >= 0.3 & comp$comp_ratio < 0.4, '< 0.4', comp$ratio)
comp$ratio = ifelse(comp$comp_ratio >= 0.4 & comp$comp_ratio < 0.5, '< 0.5', comp$ratio)
comp$ratio = ifelse(comp$comp_ratio >= 0.5 & comp$comp_ratio < 0.6, '< 0.6', comp$ratio)
comp$ratio = ifelse(comp$comp_ratio >= 0.6 & comp$comp_ratio < 0.7, '< 0.7', comp$ratio)
comp$ratio = ifelse(comp$comp_ratio >= 0.7 & comp$comp_ratio < 0.8, '< 0.8', comp$ratio)
comp$ratio = ifelse(comp$comp_ratio >= 0.8, '>= 0.8', comp$ratio)

# Join 
DS = merge(x = DS, y = comp, by = "comp_ratio", all = TRUE)

# Set colour 
colr = brewer.pal(7, "Set1") 

# Plot
DS %>%
  ggplot(aes(x=new_payload, y=original_payload, fill=ratio)) +
  geom_point(alpha=6, shape=21, color="black", stroke = .1) +
  scale_fill_manual(values=colr) +
  xlab("New payloads") +
  ylab("Original payloads") +
  labs(fill = "Compression Ratio")

