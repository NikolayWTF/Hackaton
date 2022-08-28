package com.example.npaassistant

import android.graphics.Color
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.npaassistant.databinding.OutputItemBinding

class OutputRCAdapter : ListAdapter<OutputRC, OutputRCAdapter.ItemHolder>(ItemComparator()) {

    class ItemHolder(private val binding: OutputItemBinding) : RecyclerView.ViewHolder(binding.root)
    {
        fun bind(out: OutputRC) = with(binding){
            tClassId.text = out.id
            tClassValue.text = out.value
            if (out.value.toFloat() < 0.55){
                tClassValue.setBackgroundColor(Color.RED)
            }
            else{
                if(out.value.toFloat() < 0.7){
                    tClassValue.setBackgroundColor(Color.YELLOW)
                }
                else{
                    tClassValue.setBackgroundColor(Color.GREEN)
                }
            }
        }
        companion object{
            fun create(parent: ViewGroup): ItemHolder{
                return ItemHolder(OutputItemBinding.inflate(LayoutInflater.from(parent.context), parent, false))

            }
        }
    }

    class ItemComparator : DiffUtil.ItemCallback<OutputRC>(){
        override fun areItemsTheSame(oldItem: OutputRC, newItem: OutputRC): Boolean {
            return oldItem == newItem
        }

        override fun areContentsTheSame(oldItem: OutputRC, newItem: OutputRC): Boolean {
            return oldItem == newItem
        }

    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ItemHolder {
        return ItemHolder.create(parent)
    }

    override fun onBindViewHolder(holder: ItemHolder, position: Int) {
        holder.bind(getItem(position))
    }
}